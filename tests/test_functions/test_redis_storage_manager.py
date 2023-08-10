from app.services import redis_storage_manager


def test_redist_storage():
    training_session_id = "04d3f707-ed68-4b2d-a91a-0ae200c5c7d3"
    alias = "B"
    code = "print('hello!')"
    redis_storage_manager.codesnap.set(training_session_id, alias, code)
    assert code == redis_storage_manager.codesnap.get(training_session_id, alias)