from app.services.redis_storage import RedisStorage


def test_redist_storage():
    redis_storage = RedisStorage()
    key = "04d3f707-ed68-4b2d-a91a-0ae200c5c7d3"
    value = "hello"
    redis_storage.set_value(key, value)

    assert value == redis_storage.get_value(key)