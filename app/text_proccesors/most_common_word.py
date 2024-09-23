from app.db import models

from .celery import celery
from .find_words import find_word_offsets_in_text


@celery.task(name="most_common_word")
def get_article_with_most_occurences_of_word(word: str, articles: list[models.Article]):
    max_occurences = 0
    article_id = None
    for article in articles:
        number_of_occurences = len(find_word_offsets_in_text(word, article.content))
        if number_of_occurences > max_occurences:
            max_occurences = number_of_occurences
            article_id = article.id
    return article_id
