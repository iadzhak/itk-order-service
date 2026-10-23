from uuid import UUID

from app.application.ports.clients import CatalogServicePort, PaymentServicePort
from app.domain.exceptions import PaymentServiceError


class InMemoryCatalogService(CatalogServicePort):
    def __init__(self, items: dict | None = None) -> None:
        self._items = items if items is not None else {}

    async def get_item(self, item_id: UUID) -> CatalogServicePort.ItemDTO | None:
        return self._items.get(item_id)


class InMemoryPaymentService(PaymentServicePort):
    def __init__(self, response: bool = True) -> None:
        self._response = response

    async def create_payment(self, data: PaymentServicePort.PaymentDTO) -> bool:
        if not self._response:
            raise PaymentServiceError()
        return self._response
