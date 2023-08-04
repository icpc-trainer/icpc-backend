from .ping import router as ping_router


list_of_routes = [
    ping_router,
]


__all__ = [
    "list_of_routes",
]
