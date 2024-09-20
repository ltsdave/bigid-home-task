import asyncio

import uvicorn
from fastapi import APIRouter, FastAPI

from app.db import models
from app.db.database import async_engine

from .routers import articles, comments, users


async def main():
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    app = FastAPI()
    router_v1 = APIRouter(prefix="/v1")
    router_v1.include_router(articles.router)
    router_v1.include_router(comments.router)
    router_v1.include_router(users.router)
    app.include_router(router_v1)

    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
