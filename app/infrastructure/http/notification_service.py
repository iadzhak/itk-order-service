from http import HTTPStatus

from httpx import AsyncClient, AsyncHTTPTransport

from app.application.ports.clients import NotificationServicePort
from app.infrastructure.logging import get_logger
from app.settings import conf

logger = get_logger(__name__)


class NotificationService(NotificationServicePort):
    CREATE_NOTIFICATION_URL = '/api/notifications'

    def __init__(
        self,
        base_url: str,
        api_key: str,
        max_retries: int,
    ):
        self._base_url = base_url
        self._headers = {'X-API-Key': api_key}
        self._retries = max_retries

    async def notify(
        self, notification: NotificationServicePort.NotificationDTO
    ) -> None:
        async with AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            transport=AsyncHTTPTransport(retries=self._retries),
        ) as client:
            response = await client.post(
                self.CREATE_NOTIFICATION_URL, json=notification.model_dump()
            )
            if response.status_code != HTTPStatus.CREATED:
                logger.error(
                    f'Ошибка отправки уведомления. Статус: {response.status_code} Ответ: {response.json()}'
                )


def get_notification_service() -> NotificationService:
    return NotificationService(
        base_url=conf.notification_url,
        api_key=conf.notification_key,
        max_retries=conf.max_retries,
    )
