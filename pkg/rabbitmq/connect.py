import pika


# สร้างการเชื่อมต่อกับ RabbitMQ (ระบุ host, port, และ credentials)
def connect():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",  # เช่น 'localhost' หรือ IP อื่น
            port=5672,  # RabbitMQ default port คือ 5672
            virtual_host="dev",
            credentials=pika.PlainCredentials(
                username="admin",
                password="password",
            ),
        )
    )
