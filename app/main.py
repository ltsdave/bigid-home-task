import asyncio
import logging

import uvicorn
from fastapi import APIRouter, FastAPI

from app.consts import APP_HOST_ENV_NAME, APP_PORT_ENV_NAME, LOGGER_ENV_NAME
from app.db import models
from app.db.database import async_engine
from app.utils import get_env_var

from .routers import articles, comments, users

logger = logging.getLogger(get_env_var(LOGGER_ENV_NAME))


async def main():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        logger.info("created tables")

    app = FastAPI()
    router_v1 = APIRouter(prefix="/v1")
    router_v1.include_router(articles.router)
    router_v1.include_router(comments.router)
    router_v1.include_router(users.router)
    app.include_router(router_v1)

    config = uvicorn.Config(
        app, host=get_env_var(APP_HOST_ENV_NAME), port=int(get_env_var(APP_PORT_ENV_NAME))
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
