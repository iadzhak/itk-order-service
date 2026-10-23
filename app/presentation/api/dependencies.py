from typing import Annotated

from fastapi import Depends

from app.application.ports.clients import CatalogServicePort, PaymentServicePort
from app.application.ports.uow import UnitOfWorkPort
from app.application.usecases.create_order import CreateOrderUseCase
from app.application.usecases.get_order import GetOrderUseCase
from app.infrastructure.http.catalog_service import get_catalog_service
from app.infrastructure.http.payment_service import get_payment_service
from app.infrastructure.presistance.uow import get_unit_of_work

UnitOfWorkDep = Annotated[UnitOfWorkPort, Depends(get_unit_of_work)]
CatalogServiceDep = Annotated[CatalogServicePort, Depends(get_catalog_service)]
PaymentServiceDep = Annotated[PaymentServicePort, Depends(get_payment_service)]


def get_create_order_use_case(
    uow: UnitOfWorkDep,
    catalog: CatalogServiceDep,
    payment: PaymentServiceDep,
):
    return CreateOrderUseCase(uow, catalog, payment)


def get_get_order_use_case(uow: UnitOfWorkDep):
    return GetOrderUseCase(uow)


CreateOrderUseCaseDep = Annotated[
    CreateOrderUseCase, Depends(get_create_order_use_case)
]
GetOrderUseCaseDep = Annotated[GetOrderUseCase, Depends(get_get_order_use_case)]
