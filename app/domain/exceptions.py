from uuid import UUID


class ItemNotFound(Exception):
    def __init__(self, item_id: UUID) -> None:
        super().__init__(f'Товар с id {item_id!r} не найден!')


class ItemNotEnoughQuantity(Exception):
    def __init__(self, item_name: str, requested_qty: int, available_qty: int) -> None:
        super().__init__(
            f'Недостаточно товара {item_name!r}: запрошено {requested_qty}, '
            f'доступно {available_qty}'
        )


class OrderNotFound(Exception):
    def __init__(self, order_id: UUID) -> None:
        super().__init__(f'Ордер с id {order_id!r} не найден')


class IdempotencyError(Exception):
    def __init__(self, idempotency_key: UUID) -> None:
        super().__init__(
            f'Повторная отправка с другими данными для ключа {idempotency_key!r}'
        )
