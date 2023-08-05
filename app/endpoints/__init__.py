from .ping import router as ping_router
from .ws.lobby import router as lobby_router
from .ws.training import router as training_router


list_of_routes = [
    ping_router,
    lobby_router,
    training_router,
]


__all__ = [
    "list_of_routes",
]
