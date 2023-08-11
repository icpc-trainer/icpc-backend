from .ping import router as ping_router
from .auth.user import router as user_router
from .contest.contest import router as contest_router
from .contest.standings import router as standing_router
from .contest.problems import router as problems_router
from .trainings.submissions import router as submission_router
from .trainings.training_session import router as training_session_router
from .trainings.comment import router as comment_router
from .team.team import router as team_router
from .ws.lobby import router as ws_lobby_router
from .ws.training import router as ws_training_router


list_of_routes = [
    ping_router,
    contest_router,
    standing_router,
    problems_router,
    submission_router,
    ws_lobby_router,
    ws_training_router,
    training_session_router,
    comment_router,
    user_router,
    team_router,
]


__all__ = [
    "list_of_routes",
]
