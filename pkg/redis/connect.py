# pip install redis

import redis


class Redis:
    def __init__(self):
        self.redis_client = redis.Redis(
            host="localhost", port=6379, decode_responses=True
        )

    def set(self, key: str, value: str) -> None:
        return self.redis_client.set(key, value)

    def get(self, key: str) -> str:
        return self.redis_client.get(key)

    def hset(self, name: str, key: str, value: str) -> None:
        return self.redis_client.hset(name, key, value)
