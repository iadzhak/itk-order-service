from uuid import UUID

from fastapi import APIRouter, status

from app.application.ports.usecases import CreateOrderDTO
from app.domain.models import Order
from app.presentation.api.dependencies import CreateOrderUseCaseDep, GetOrderUseCaseDep

router = APIRouter()


class CreateOrderRequest(CreateOrderDTO):
    pass


class CreateOrderResponse(Order):
    pass


class GetOrderResponse(Order):
    pass


@router.post(
    '', response_model=CreateOrderResponse, status_code=status.HTTP_201_CREATED
)
async def create_order(order: CreateOrderRequest, use_case: CreateOrderUseCaseDep):
    return await use_case(CreateOrderDTO.model_validate(order))


@router.get('/{order_id}', response_model=GetOrderResponse)
async def get_order(order_id: UUID, use_case: GetOrderUseCaseDep):
    return await use_case(order_id)
