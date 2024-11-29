# ต้องสร้างไฟล์ __init__.py เพื่อให้ Python รู้จัก package นี้


# นำเข้า connect จาก connect.py และทำให้ export ไปยัง rabbitmq package
from .connect import connect
from .rabbitmq import RabbitMQ
