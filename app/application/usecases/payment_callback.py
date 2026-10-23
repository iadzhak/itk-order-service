from app.application.ports.uow import UnitOfWorkPort
from app.application.ports.usecases import PaymentDTO, PaymentStatus
from app.domain.models import OrderStatus
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)


class PaymentCallback:
    def __init__(self, uow: UnitOfWorkPort):
        self._uow = uow

    async def __call__(self, payment: PaymentDTO) -> None:
        async with self._uow() as uow:
            order = await uow.orders.get_by_id(payment.order_id, OrderStatus.NEW)
            if not order:
                return

            if payment.status == PaymentStatus.SUCCEEDED:
                order.set_paid()
            elif payment.status == PaymentStatus.FAILED:
                order.set_cancelled()
            else:
                logger.warning(
                    f'Неизвестный статус платежа: {payment.status} для ордера: {payment.order_id}'
                )
                return

            await uow.orders.update(order)

            await uow.commit()
