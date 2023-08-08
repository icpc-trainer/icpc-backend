from .ping import router as ping_router
from .standings.standings_my import router as standing_router
from .trainings.training_session import router as training_session_router
from .ws.lobby import router as ws_lobby_router
from .ws.training import router as ws_training_router


list_of_routes = [
    ping_router,
    standing_router,
    ws_lobby_router,
    ws_training_router,
    training_session_router,
]


__all__ = [
    "list_of_routes",
]
