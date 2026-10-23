from http import HTTPStatus

from httpx import AsyncClient, AsyncHTTPTransport

from app.application.ports.clients import PaymentServicePort
from app.domain.exceptions import PaymentServiceError
from app.infrastructure.logging import get_logger
from app.settings import conf

logger = get_logger(__name__)


class PaymentService(PaymentServicePort):
    CREATE_PAYMENT_URL: str = '/api/payments'

    def __init__(self, base_url: str, api_key: str, max_retries: int) -> None:
        self._base_url = base_url
        self._headers = {'X-API-Key': api_key}
        self.max_retries = max_retries

    async def create_payment(self, data: PaymentServicePort.PaymentDTO) -> bool:
        async with AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            transport=AsyncHTTPTransport(retries=self.max_retries),
        ) as client:
            response = await client.post(
                self.CREATE_PAYMENT_URL, data=data.model_dump()
            )
            if response.status_code == HTTPStatus.CREATED:
                return True
            logger.error(
                'Не удалось создать платеж. Статус: %s; Ответ: %s',
                response.status_code,
                response.json(),
            )
            raise PaymentServiceError()


def get_payment_service() -> PaymentService:
    return PaymentService(
        base_url=conf.payment_url,
        api_key=conf.payment_key,
        max_retries=conf.max_retries,
    )
