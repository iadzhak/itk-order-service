from uuid import UUID


class OrderNotFound(Exception):
    def __init__(self, order_id: UUID) -> None:
        super().__init__(f'Ордер с id {order_id!r} не найден')
