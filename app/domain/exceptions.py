from uuid import UUID


class OrderNotFound(Exception):
    def __init__(self, order_id: UUID) -> None:
        super().__init__(f'Ордер с id {order_id!r} не найден')


class IdempotencyError(Exception):
    def __init__(self, idempotency_key: UUID) -> None:
        super().__init__(
            f'Повторная отправка с другими данными для ключа {idempotency_key!r}'
        )
