from .contest_api_manager import ContestApiManager
from .proxy_manager import ProxyManager
from .connection_manager import ConnectionManager
from .contest_training_repository import ContestTrainingRepository

lobby_manager = ConnectionManager()
training_manager = ConnectionManager()

__all__ = [
    "ContestApiManager",
    "ProxyManager"
    "ConnectionManager",
    "lobby_manager",
    "training_manager",
    "ContestTrainingRepository",
]
