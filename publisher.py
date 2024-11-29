from pkg.rabbitmq import RabbitMQ
import json
from datetime import datetime


def publish():
    # ส่งข้อมูล 10 ครั้ง
    rabbitmq = RabbitMQ("hello-py")
    for i in range(10):

        message = {
            "id": i,
            "message": f"Hello world {i}",
            "timestamp": datetime.now().isoformat(),
            "payment_status": "wait_payment",
        }

        if i == 3:
            message["payment_status"] = "payment_success"

        try:
            rabbitmq.publish(
                exchange="logs",
                routing_key="routing-hello",
                message=json.dumps(message),
            )
            print(f"[x] Published Order Done. [{message}]")
        except Exception as e:
            print(f"[x] Published Order Error. [{e}]")

    rabbitmq.close()
    print(f"[x] Sent Completed!")


publish()
