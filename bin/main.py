import asyncio

import uvicorn

from app import conf, create_app


async def main() -> None:
    app = create_app()

    api_task = asyncio.create_task(
        uvicorn.Server(uvicorn.Config(app, host=conf.host, port=conf.port)).serve()
    )
    await api_task


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
