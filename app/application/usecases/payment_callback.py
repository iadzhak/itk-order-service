from app.application.ports.clients import NotificationServicePort
from app.application.ports.uow import UnitOfWorkPort
from app.application.ports.usecases import PaymentDTO, PaymentStatus
from app.domain.models import EventType, OrderStatus
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)


class PaymentCallback:
    def __init__(self, uow: UnitOfWorkPort, notify: NotificationServicePort):
        self._uow = uow
        self._notify = notify

    async def __call__(self, payment: PaymentDTO) -> None:
        paid = False
        async with self._uow() as uow:
            order = await uow.orders.get_by_id(payment.order_id, OrderStatus.NEW)
            if not order:
                return

            if payment.status == PaymentStatus.SUCCEEDED:
                payload = order.set_paid()

                # order.paid event
                await uow.outbox.create(
                    uow.outbox.CreateDTO(
                        event_type=EventType.ORDER_PAID, payload=payload
                    )
                )
                paid = True
            elif payment.status == PaymentStatus.FAILED:
                order.set_cancelled()
            else:
                logger.warning(
                    f'Неизвестный статус платежа: {payment.status} для ордера: {payment.order_id}'
                )
                return

            await uow.orders.update(order)

            await uow.commit()
        if paid:
            await self._notify.notify_paid(payment.order_id)
