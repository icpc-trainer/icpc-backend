from .ping import router as ping_router
from .standings.standings_my import router as standing_router


list_of_routes = [
    ping_router,
    standing_router,
]


__all__ = [
    "list_of_routes",
]
