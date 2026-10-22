from uuid import UUID

from app.application.ports.clients import CatalogServicePort


class InMemoryCatalogService(CatalogServicePort):
    def __init__(self, items: dict | None = None) -> None:
        self._items = items if items is not None else {}

    async def get_item(self, item_id: UUID) -> CatalogServicePort.ItemDTO | None:
        return self._items.get(item_id)
