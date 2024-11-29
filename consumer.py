from pkg.rabbitmq import RabbitMQ
from pkg.redis import Redis
from pkg.mongo import MongoDB
import json


# process ที่จะทำคือ
# 1. เช็คจาก redis ก่อนว่ามีข้อมูล key แล้ว status เป็น wait_payment ไม่ต้องทำอะไร
# 2. แต่ถ้าไม่มีบน redis => ให้ไปลง mongodb ด้วย status เป็น wait_payment และ save on redis ด้วย status ตามที่ส่งมา
# 3. ถ้ามีบน redis แต่สถานที่ส่งมาเป็น payment_success ให้อัพเดทลง mongodb และอัพเดทลง redis ด้วย status เป็น payment_success

REDIS_KEY = "order"

# Connect Redis
redis_client = Redis()

# Connect MongoDB
mongo_client = MongoDB()
mongo_client.get_collection("mydatabase", "mycollection")


# process callback
def callback(ch, method, _, body):
    # แปลง json
    message = json.loads(body)

    order_id = message["id"]

    # เช็คบน redis ว่ามีข้อมูลบน redis หรือไม่
    redis_data = redis_client.get(f"{REDIS_KEY}:{order_id}")

    # แปลง json เฉพาะข้อมูลที่มีอยู่บน redis
    redis_data_json = None
    if redis_data != None:
        redis_data_json = json.loads(redis_data)

    # เฉพาะข้อมูลที่มีอยู่บน redis และสถานะเป็น wait_payment
    if redis_data:
        print(
            f"{message['id']} found in redis , redis_status:{redis_data_json['payment_status']} , message_status:{message['payment_status']}"
        )

        # ถ้ามีให้เช็คสถานะก่อนว่าอยู่ในสถานะไหน ให้ทำเฉพาะที่บน redis อยู่ในสถานะ wait_payment
        if (
            message["payment_status"] == "payment_success"
            and redis_data_json["payment_status"] == "wait_payment"
        ):
            mongo_client.update_one(
                {"id": order_id}, {"$set": {"payment_status": "payment_success"}}
            )
            redis_client.set(f"{REDIS_KEY}:{order_id}", json.dumps(message))

        ch.basic_ack(delivery_tag=method.delivery_tag)
        return  # end process

    # ถ้าไม่มีบน redis ให้ลง mongodb
    mongo_client.insert_one(
        {"id": order_id, "payment_status": message["payment_status"]}
    )
    redis_client.set(f"{REDIS_KEY}:{order_id}", json.dumps(message))

    # Acknowledge message
    ch.basic_ack(delivery_tag=method.delivery_tag)


try:
    rabbitmq = RabbitMQ("hello-py")
    rabbitmq.consume(callback)
except Exception as e:
    print(f"[x] Consume Order Error. [{e}]")
