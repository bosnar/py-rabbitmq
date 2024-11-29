from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://root:root@localhost:27017")
        self.collection = None

    def get_collection(self, db: str, collection: str):
        # เลือก Collection
        db_instance = self.client[db]  # ชื่อฐานข้อมูล (สร้างใหม่หากยังไม่มี)
        self.collection = db_instance[collection]

    def insert_one(self, data: dict):
        return self.collection.insert_one(data)

    def update_one(self, filter: dict, data: dict):
        return self.collection.update_one(filter, data)
