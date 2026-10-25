import asyncio

import uvicorn

from app import conf, create_app
from app.inbox_worker import get_inbox_worker
from app.infrastructure.kafka_consumer import get_kafka_consumer
from app.outbox_worker import create_outbox_worker


async def main() -> None:
    app = create_app()
    outbox_worker = create_outbox_worker()
    inbox_consumer = get_kafka_consumer()
    inbox_worker = get_inbox_worker()
    api_task = asyncio.create_task(
        uvicorn.Server(uvicorn.Config(app, host=conf.host, port=conf.port)).serve()
    )

    await asyncio.gather(
        api_task, outbox_worker.run(), inbox_consumer.run(), inbox_worker.run()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
