from .ping import router as ping_router
from .auth.user import router as user_router 
from .contest.standings import router as standing_router
from .contest.problems import router as problems_router
from .contest.submissions import router as submission_router
from .trainings.training_session import router as training_session_router
from .ws.lobby import router as ws_lobby_router
from .ws.training import router as ws_training_router


list_of_routes = [
    ping_router,
    standing_router,
    problems_router,
    submission_router,
    ws_lobby_router,
    ws_training_router,
    training_session_router,
    user_router,
]


__all__ = [
    "list_of_routes",
]
