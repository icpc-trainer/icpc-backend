from .redis_storage import RedisStorage


class CodeSnapManager:
    def __init__(self, redis_storage):
        self.redis_storage = redis_storage
        self.prefix = "codesnaps"

    def get_key(self, training_session_id, alias):
        return f"{self.prefix}:{training_session_id}:{alias}"

    def set(self, training_session_id, alias, code):
        key = self.get_key(training_session_id, alias)
        return self.redis_storage.set_value(key, code)

    def get(self, training_session_id, alias):
        key = self.get_key(training_session_id, alias)
        code = self.redis_storage.get_value(key)
        return code if code else ""


class ControllerManager:
    def __init__(self, redis_storage):
        self.redis_storage = redis_storage
        self.prefix = "controllers"

    def get_key(self, training_session_id):
        return f"{self.prefix}:{training_session_id}"

    def set(self, training_session_id, owner):
        key = self.get_key(training_session_id)
        return self.redis_storage.set_value(key, owner)

    def get(self, training_session_id):
        key = self.get_key(training_session_id)
        owner = self.redis_storage.get_value(key)
        return owner if owner else ""


class RedisStorageManager:
    def __init__(self):
        self.redis_storage = RedisStorage()
        self.codesnap = CodeSnapManager(self.redis_storage)
        self.controller = ControllerManager(self.redis_storage)
