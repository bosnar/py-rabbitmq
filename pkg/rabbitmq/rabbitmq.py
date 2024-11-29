from pkg.rabbitmq import connect


class RabbitMQ:
    # กำหนดค่าเริ่มต้น
    def __init__(self, queue: str):
        self.connection = connect()
        self.queue_name = queue

    def get_queue_name(self):
        return self.queue_name

    def get_connection(self):
        return self.connection

    def close(self):
        self.connection.close()

    # publish message
    def publish(self, exchange: str, routing_key: str, message: str):
        # ประกาศคิว
        self.declare_queue()
        # ประกาศ exchange
        self.exchange_declare(exchange, "direct")
        # bind queue to exchange
        self.bind_queue(exchange, routing_key)
        # publish message
        self.connection.channel().basic_publish(
            exchange=exchange, routing_key=routing_key, body=message
        )

    def declare_queue(self):
        self.connection.channel().queue_declare(
            queue=self.queue_name, durable=True, auto_delete=False
        )

    def bind_queue(self, exchange: str, routing_key: str):
        self.connection.channel().queue_bind(
            exchange=exchange, queue=self.queue_name, routing_key=routing_key
        )

    def exchange_declare(self, exchange: str, exchange_type: str):
        self.connection.channel().exchange_declare(exchange, exchange_type)

    def consume(self, callback):
        # ประกาศ channel เดียวกัน
        channel = self.connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=False
        )
        channel.start_consuming()
