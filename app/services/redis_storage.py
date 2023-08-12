import redis

from app.config import settings


class RedisStorage:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=0,
        )

    def set_value(self, key, value):
        try:
            self.redis_client.set(key, value)
            return True
        except Exception as e:
            print(f"Error setting value: {e}")
            return False

    def get_value(self, key):
        try:
            value = self.redis_client.get(key)
            if value is not None:
                return value.decode('utf-8')
            else:
                return None
        except Exception as e:
            print(f"Error getting value: {e}")
            return None