from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, ConfigDict

from app.application.ports.usecases import CreateOrderDTO
from app.domain.models import OrderStatus
from app.presentation.api.dependencies import CreateOrderUseCaseDep, GetOrderUseCaseDep

router = APIRouter()


class CreateOrderRequest(CreateOrderDTO):
    pass


class OrderResponse(BaseModel):
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


@router.post('', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrderRequest, use_case: CreateOrderUseCaseDep):
    return await use_case(CreateOrderDTO.model_validate(order))


@router.get('/{order_id}', response_model=OrderResponse)
async def get_order(order_id: UUID, use_case: GetOrderUseCaseDep):
    return await use_case(order_id)
