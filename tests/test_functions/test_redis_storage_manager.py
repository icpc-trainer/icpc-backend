from app.services import RedisStorageManager


def test_code_snap_manager():
    redis_storage_manager = RedisStorageManager()
    training_session_id = "04d3f707-ed68-4b2d-a91a-0ae200c5c7d3"
    alias = "B"
    code = "print('hello!')"
    redis_storage_manager.codesnap.set(training_session_id, alias, code)
    assert code == redis_storage_manager.codesnap.get(training_session_id, alias)


def test_controller_manager():
    redis_storage_manager = RedisStorageManager()
    training_session_id = "04d3f707-ed68-4b2d-a91a-0ae200c5c7d3"
    user_id = "326882283"
    redis_storage_manager.controller.set(training_session_id, user_id)
    assert user_id == redis_storage_manager.controller.get(training_session_id)