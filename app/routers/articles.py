import logging

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.consts import LOGGER_ENV_NAME
from app.db import crud, schemas
from app.db.database import get_session
from app.text_proccesors.find_words import build_word_occurences_object
from app.text_proccesors.most_common_word import get_article_with_most_occurences_of_word
from app.types import WordsOccurecnes
from app.utils import get_env_var
from app.words_cache.words_cache import WordsCache

router = APIRouter(prefix="/articles")
logger = logging.getLogger(get_env_var(LOGGER_ENV_NAME))
words_cache = WordsCache()


@router.post("/", tags=["articles"], response_model=schemas.Article)
async def create_article(article_create: schemas.ArticleCreate, session: AsyncSession = Depends(get_session)):
    existing_article = await crud.articles.get_by_title(session=session, title=article_create.title)
    if existing_article:
        logger.error(f"tried to create an already published article {article_create.title}")
        raise HTTPException(status_code=400, detail="Article already published")
    user = await crud.users.get_one(session=session, user_id=article_create.author_id)
    if not user:
        logger.error(f"tried to create an article of a non existing author {article_create.author_id}")
        raise HTTPException(status_code=400, detail="Article is written by a non existing author")

    article = await crud.articles.create(session=session, article_create=article_create)
    logger.info(f"created a new article, clearing words cache")
    words_cache.clear()
    return article


@router.get("/", tags=["articles"], response_model=list[schemas.Article])
async def get_articles(author_id: int = None, session: AsyncSession = Depends(get_session)):
    articles = await crud.articles.get_all(session=session, author_id=author_id)
    logger.info("finished fetching articles")
    return articles


@router.get("/{article_id}", tags=["articles"], response_model=schemas.Article)
async def get_article(article_id: int, session: AsyncSession = Depends(get_session)):
    article = await crud.articles.get_one(session=session, article_id=article_id)
    if article is None:
        logger.error(f"tried to fetch a non existing article with id {article_id}")
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/find_words", tags=["articles"], response_model=WordsOccurecnes)
async def find_words(words: list[str], session: AsyncSession = Depends(get_session)):
    words_occurecnes = words_cache.get_words_occurences(words)
    logger.info(f"finished quering cache for word occurnces")

    words_outside_cache = words_cache.get_words_outside_cache(words)
    if words_outside_cache:
        articles = await crud.articles.get_all(session=session)
        articles_list = [article for article in articles]
        words_occurecnes_outside_cache = build_word_occurences_object(words_outside_cache, articles_list)
        logger.info(f"finished building word occurences from database")
        words_occurecnes.extend(words_occurecnes_outside_cache)
        words_cache.update_cache(words_occurecnes_outside_cache, words_outside_cache)

    return words_occurecnes
