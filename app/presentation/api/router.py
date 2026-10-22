from fastapi import APIRouter

from app.presentation.api.health import router as health_router
from app.presentation.api.orders import router as orders_router

router = APIRouter(prefix='/api')
router.include_router(orders_router, prefix='/orders', tags=['orders'])
router.include_router(health_router, prefix='/health', tags=['health'])
