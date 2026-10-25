from uuid import UUID


class ItemError(Exception):
    pass


class ItemNotFound(ItemError):
    def __init__(self, item_id: UUID) -> None:
        super().__init__(f'Товар с id {item_id!s} не найден!')


class ItemNotEnoughQuantity(ItemError):
    def __init__(self, item_name: str, requested_qty: int, available_qty: int) -> None:
        super().__init__(
            f'Недостаточно товара {item_name!r}: запрошено {requested_qty}, '
            f'доступно {available_qty}'
        )


class OrderNotFound(Exception):
    def __init__(self, order_id: UUID) -> None:
        super().__init__(f'Ордер с id {order_id!s} не найден')


class IdempotencyError(Exception):
    def __init__(self, idempotency_key: str) -> None:
        super().__init__(
            f'Повторная отправка с другими данными для ключа {idempotency_key!r}'
        )


class ExternalServiceError(Exception):
    NAME = ''


class CatalogServiceError(ExternalServiceError):
    NAME = 'Каталог'


class PaymentServiceError(ExternalServiceError):
    NAME = 'Сервис платежей'


class NotificationError(Exception):
    pass
