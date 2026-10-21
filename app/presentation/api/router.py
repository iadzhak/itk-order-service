from fastapi import APIRouter

from app.presentation.api.orders import router as orders_router

router = APIRouter(prefix='/api')
router.include_router(orders_router, prefix='/orders', tags=['orders'])
