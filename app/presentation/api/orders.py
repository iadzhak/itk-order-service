from uuid import UUID

from fastapi import APIRouter, status

from app.application.ports.usecases import CreateOrderDTO
from app.domain.models import Order

router = APIRouter()


class CreateOrderRequest(CreateOrderDTO):
    pass


class CreateOrderResponse(Order):
    pass


class GetOrderResponse(Order):
    pass


@router.get('', response_model=CreateOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrderRequest):
    pass


@router.get('/{order_id}', response_model=GetOrderResponse)
async def get_order(order_id: UUID):
    pass
