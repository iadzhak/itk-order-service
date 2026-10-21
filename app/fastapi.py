from fastapi import FastAPI

from app.presentation.api import main_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(main_router)
    return app
