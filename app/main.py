import uvicorn
from fastapi import APIRouter, FastAPI

from app.db import models
from app.db.database import engine

from .routers import articles, comments, users

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(articles.router)
router_v1.include_router(comments.router)
router_v1.include_router(users.router)
app.include_router(router_v1)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
