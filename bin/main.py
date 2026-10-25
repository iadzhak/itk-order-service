import asyncio

import uvicorn

from app import conf, create_app
from app.outbox_worker import create_outbox_worker


async def main() -> None:
    app = create_app()
    outbox_worker = create_outbox_worker()

    api_task = asyncio.create_task(
        uvicorn.Server(uvicorn.Config(app, host=conf.host, port=conf.port)).serve()
    )

    await asyncio.gather(api_task, outbox_worker.run())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
