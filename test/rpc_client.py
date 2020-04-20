import pika
import uuid


class AuthClient(object):

    def __init__(self):
        credential = pika.PlainCredentials('admin', 'admin')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='172.18.0.4', port=5672, virtual_host='logi-rabbitmq', credentials=credential))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self):
        import json
        payload = json.dumps(
            {
                'username': "admin",
                'password': "admin"
            }
        )
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='auth_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(payload))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


auth_rpc = AuthClient()

response = auth_rpc.call()
print(" [.] Got %s" % response)
