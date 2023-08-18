import json

from .redis_storage import RedisStorage


# TODO: Отрефакторить

class CodeSnapManager:
    def __init__(self, redis_storage, prefix):
        self.redis_storage = redis_storage
        self.prefix = prefix

    def set(self, training_session_id, alias, code) -> None:
        key = f"{self.prefix}:{training_session_id}:{alias}"
        self.redis_storage.set_value(key, code)

    def get(self, training_session_id, alias) -> str:
        key = f"{self.prefix}:{training_session_id}:{alias}"
        code = self.redis_storage.get_value(key)
        return code if code else ""


class ControllerManager:
    def __init__(self, redis_storage, prefix):
        self.redis_storage = redis_storage
        self.prefix = prefix

    def set(self, training_session_id, owner) -> None:
        key = f"{self.prefix}:{training_session_id}"
        self.redis_storage.set_value(key, owner)

    def get(self, training_session_id) -> str:
        key = f"{self.prefix}:{training_session_id}"
        owner = self.redis_storage.get_value(key)
        return owner if owner else ""


class UsersManager:
    def __init__(self, redis_storage, prefix):
        self.redis_storage = redis_storage
        self.prefix = prefix

    def add_user(self, id, user):
        key = f"{self.prefix}:{id}"
        user_id = user.get('id')

        if user_id is None:
            raise ValueError("Item must have an 'id' field.")

        users = self.get_users(id)
        user_ids = [u.get('id') for u in users]

        if user_id not in user_ids:
            users.append(user)
            self.set_users(key, users)

    def get_users(self, id):
        key = f"{self.prefix}:{id}"
        users = self.redis_storage.get_value(key)
        if users is None:
            return []
        return json.loads(users)

    def set_users(self, key, users):
        self.redis_storage.set_value(key, json.dumps(users, ensure_ascii=False))

    def remove_user(self, id, user_id):
        key = f"{self.prefix}:{id}"
        users = self.get_users(id)
        users = [user for user in users if user.get('id') != user_id]
        self.set_users(key, users)


class AssigmentManager:
    def __init__(self, redis_storage, prefix):
        self.redis_storage = redis_storage
        self.prefix = prefix

    def set(self, training_session_id, alias, user) -> None:
        key = f"{self.prefix}:{training_session_id}:{alias}"
        self.redis_storage.set_value(key, json.dumps(user, ensure_ascii=False))

    def get(self, training_session_id, alias) -> str:
        key = f"{self.prefix}:{training_session_id}:{alias}"
        user = self.redis_storage.get_value(key)
        return json.loads(user) if user else None


class SelectedContestManager:
    def __init__(self, redis_storage, prefix):
        self.redis_storage = redis_storage
        self.prefix = prefix

    def set(self, team_id, contest_id) -> None:
        key = f"{self.prefix}:{team_id}"
        self.redis_storage.set_value(key, contest_id)

    def get(self, team_id) -> str:
        key = f"{self.prefix}:{team_id}"
        contest_id = self.redis_storage.get_value(key)
        return contest_id


class RedisStorageManager:
    def __init__(self):
        self.redis_storage = RedisStorage()
        self.codesnap = CodeSnapManager(self.redis_storage, "codesnaps")
        self.controller = ControllerManager(self.redis_storage, "controllers")
        self.lobby_users = UsersManager(self.redis_storage, "users:lobbies")
        self.training_users = UsersManager(self.redis_storage, "users:trainings")
        self.assigments = AssigmentManager(self.redis_storage, "assigments")
        self.selected_contests = SelectedContestManager(self.redis_storage, "selected_contests")
