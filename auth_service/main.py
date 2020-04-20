import json
import pika

import config as cfg
import web_auth
import app_auth
from vendor import database

def get_credential(username, password):
    return pika.PlainCredentials(username, password)


def get_endpoint(endpoint_cfg):
    host = endpoint_cfg.get('address', "localhost")
    port = endpoint_cfg.get('port', 5672)
    vm_host = endpoint_cfg.get('vm_host', "")

    username = endpoint_cfg.get('user', "")
    password = endpoint_cfg.get('pass', "")
    credential = get_credential(username, password)
    return pika.ConnectionParameters(host=host,port=port, virtual_host=vm_host, credentials=credential)


class AuthService():
    def __init__(self):
        self.database = database.Posgressql(
            cfg.POSTGRESQL.get("address"),
            cfg.POSTGRESQL.get("port"),
            cfg.POSTGRESQL.get("database"),
            cfg.POSTGRESQL.get("user"),
            cfg.POSTGRESQL.get("pass")
        )

    def __on_request(self, ch, method, props, body):
        web = web_auth.WebAuth(self.database)
        app = app_auth.AppAuth(self.database)

        print(body)
        payload = json.loads(body)
        phone = payload.get('phone_number', None)
        if phone:
            response = app.login(phone)
        else:
            username = payload.get('username')
            password = payload.get('password')
            response = web.login(username, password)

        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def broker_run(self):
        endpoints = [get_endpoint(endpoint_cfg) for endpoint_cfg in cfg.HOSTS_CONFIGURATION]
        print(endpoints)
        connection = pika.BlockingConnection(endpoints)

        channel = connection.channel()

        channel.queue_declare(queue=cfg.TOPIC)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=cfg.TOPIC, on_message_callback=self.__on_request)

        print(" [x] Awaiting RPC requests")
        channel.start_consuming()


if __name__ == "__main__":
    print("Start auth service")
    auth_service = AuthService()
    auth_service.broker_run()