import logging

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.consts import LOGGER_ENV_NAME
from app.db import crud
from app.db import schemas
from app.db.database import get_session
from app.text_proccesors.most_common_word import get_article_with_most_occurences_of_word
from app.utils import get_env_var

router = APIRouter(prefix="/tasks")
logger = logging.getLogger(get_env_var(LOGGER_ENV_NAME))


@router.get("/most_common_word", tags=["tasks"], response_model=dict[str, str])
async def most_common_word(word: str, session: AsyncSession = Depends(get_session)):
    articles_models = await crud.articles.get_all(session=session)
    articles_dicts = [schemas.Article.model_validate(article).model_dump() for article in articles_models]
    task = get_article_with_most_occurences_of_word.delay(word, articles_dicts)
    logger.info(f"enqueued most_common_word task - {task.id}")
    return {"task_id": task.id}


@router.post("/most_common_word_result", tags=["tasks"], response_model=dict)
async def most_common_word_result(task_id: str):
    task_result = AsyncResult(task_id)
    result = {"task_id": task_id, "task_status": task_result.status, "task_result": task_result.result}
    logger.info(result)
    return result
