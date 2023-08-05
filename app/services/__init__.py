from .connection_manager import ConnectionManager


lobby_manager = ConnectionManager()
training_manager = ConnectionManager()

__all__ = [
    "ConnectionManager",
    "lobby_manager",
    "training_manager",
]
