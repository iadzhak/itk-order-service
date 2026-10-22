from http import HTTPStatus
from uuid import UUID

from httpx import AsyncClient

from app.application.ports.clients import CatalogServicePort
from app.settings import conf


class CatalogService(CatalogServicePort):
    GET_ITEM_URL = '/api/catalog/items/{item_id}'

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url
        self._headers = {'X-API-Key': api_key}

    async def get_item(self, item_id: UUID) -> CatalogServicePort.ItemDTO | None:
        url = self.GET_ITEM_URL.format(item_id=item_id)
        async with AsyncClient(
            base_url=self._base_url, headers=self._headers
        ) as client:
            response = await client.get(url=url, headers=self._headers)
            if response.status_code == HTTPStatus.OK:
                return CatalogServicePort.ItemDTO.model_validate(response.json())
            if response.status_code == HTTPStatus.NOT_FOUND:
                return None
            response.raise_for_status()
            return None


def get_catalog_service() -> CatalogService:
    return CatalogService(base_url=conf.catalog_url, api_key=conf.catalog_key)
