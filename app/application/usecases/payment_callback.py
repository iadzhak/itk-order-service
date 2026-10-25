from app.application.ports.uow import UnitOfWorkPort
from app.application.ports.usecases import PaymentDTO, PaymentStatus
from app.domain.models import EventType, Order, OrderStatus
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
                await uow.orders.mark_as_paid(payment.order_id)
                await uow.outbox.create(
                    uow.outbox.CreateDTO(
                        event_type=EventType.ORDER_PAID, payload=order.make_payment()
                    )
                )
                await uow.outbox.create(
                    uow.outbox.CreateDTO(
                        event_type=EventType.NOTIFICATION,
                        payload=Order.make_notification(
                            payment.order_id, OrderStatus.PAID
                        ),
                    )
                )
            elif payment.status == PaymentStatus.FAILED:
                await uow.orders.mark_as_cancelled(payment.order_id)
                await uow.outbox.create(
                    uow.outbox.CreateDTO(
                        event_type=EventType.NOTIFICATION,
                        payload=Order.make_notification(
                            payment.order_id, OrderStatus.CANCELLED, 'Платеж не прошел'
                        ),
                    )
                )
            else:
                logger.warning(
                    f'Неизвестный статус платежа: {payment.status} для ордера: {payment.order_id}'
                )
                return

            await uow.commit()
