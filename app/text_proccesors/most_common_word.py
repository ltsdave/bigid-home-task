from celery import Celery

from app.consts import CELERY_BROKER_URL_NAME, CELERY_RESULT_BACKEND_NAME
from app.utils import get_env_var

from .find_words import find_word_offsets_in_text

celery = Celery(__name__)
celery.conf.broker_url = get_env_var(CELERY_BROKER_URL_NAME)
celery.conf.result_backend = get_env_var(CELERY_RESULT_BACKEND_NAME)


@celery.task(name="most_common_word")
def get_article_with_most_occurences_of_word(word: str, articles_dicts: list[dict]):
    max_occurences = 0
    article_id = None
    for article in articles_dicts:
        number_of_occurences = len(find_word_offsets_in_text(word, article["content"]))
        if number_of_occurences > max_occurences:
            max_occurences = number_of_occurences
            article_id = article["id"]
    return article_id
