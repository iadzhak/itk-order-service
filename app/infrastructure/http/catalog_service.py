from http import HTTPStatus
from uuid import UUID

from httpx import AsyncClient, AsyncHTTPTransport

from app.application.ports.clients import CatalogServicePort
from app.domain.exceptions import CatalogServiceError
from app.infrastructure.logging import get_logger
from app.settings import conf

logger = get_logger(__name__)


class CatalogService(CatalogServicePort):
    GET_ITEM_URL = '/api/catalog/items/{item_id}'

    def __init__(self, base_url: str, api_key: str, max_retries: int) -> None:
        self._base_url = base_url
        self._headers = {'X-API-Key': api_key}
        self._max_retries = max_retries

    async def get_item(self, item_id: UUID) -> CatalogServicePort.ItemDTO | None:
        url = self.GET_ITEM_URL.format(item_id=item_id)
        async with AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            transport=AsyncHTTPTransport(retries=self._max_retries),
        ) as client:
            response = await client.get(url=url, headers=self._headers)
            if response.status_code == HTTPStatus.OK:
                return CatalogServicePort.ItemDTO.model_validate(response.json())
            if response.status_code == HTTPStatus.NOT_FOUND:
                return None
            logger.error(
                'Не удалось получить информацию из каталога. Статус: %s; Ответ: %s',
                response.status_code,
                response.json(),
            )
            raise CatalogServiceError()


def get_catalog_service() -> CatalogService:
    return CatalogService(
        base_url=conf.catalog_url,
        api_key=conf.catalog_key,
        max_retries=conf.max_retries,
    )
