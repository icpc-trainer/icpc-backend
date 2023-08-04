from fastapi import FastAPI
from uvicorn import run

from app.config import settings
from app.endpoints import list_of_routes


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Backend for implementing chat via websockets"

    app = FastAPI(
        title="FastApi-Chat",
        description=description,
        version="0.1.0",
    )
    bind_routes(app)
    app.state.settings = settings
    return app


app = get_app()


if __name__ == "__main__":
    run(
        "app.__main__:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        reload_dirs=["app", "tests"],
        log_level="debug",
    )
