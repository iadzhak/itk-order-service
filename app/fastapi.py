from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import IdempotencyError, ItemError, OrderNotFound
from app.presentation.api import main_router


def register_middlewares(app: FastAPI) -> None:
    @app.exception_handler(ItemError)
    async def handle_400(request: Request, exc: ItemError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={'details': str(exc)}
        )

    @app.exception_handler(OrderNotFound)
    async def handle_404(request: Request, exc: OrderNotFound) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={'details': str(exc)}
        )

    @app.exception_handler(IdempotencyError)
    async def handle_409(request: Request, exc: IdempotencyError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={'details': str(exc)}
        )


def create_app() -> FastAPI:
    app = FastAPI()
    register_middlewares(app)
    app.include_router(main_router)
    return app
