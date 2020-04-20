# RabbitMQ Configuration
HOSTS_CONFIGURATION = [
    {
        "address": '172.18.0.4',
        "port": 5672,
        "vm_host": "my-rabbitmq",
        "user": "admin",
        "pass": "admin"
    }
]

TOPIC = "auth_queue"

# Database configuartion
POSTGRESQL = {
    "address": "172.18.0.2",
    "port": 5432,
    "user": "postgres",
    "pass": "admin",
    "database": "postgres"
}