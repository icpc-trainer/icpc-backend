from .contest_api_manager import ContestApiManager
from .proxy_manager import ProxyManager
from .connection_manager import ConnectionManager
from .training_session_repository import TrainingSessionRepository
from .redis_storage_manager import RedisStorageManager


lobby_manager = ConnectionManager()
training_manager = ConnectionManager()
redis_storage_manager = RedisStorageManager()

__all__ = [
    "ContestApiManager",
    "ProxyManager",
    "ConnectionManager",
    "lobby_manager",
    "training_manager",
    "TrainingSessionRepository",
    "redis_storage_manager",
]
