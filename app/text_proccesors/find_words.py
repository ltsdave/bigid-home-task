from app.db import models
from app.types import WordsOccurecnes


def build_word_occurences_object(words: list[str], articles: list[models.Article]) -> WordsOccurecnes:
    words_occurences = []
    for word in words:
        word_occurences = {}
        for article in articles:
            offsets = find_word_offsets_in_text(word, article.content)
            if offsets:
                if word in word_occurences:
                    word_occurences[word].append({"article_id": article.id, "offsets": offsets})
                else:
                    word_occurences[word] = [{"article_id": article.id, "offsets": offsets}]
        if word_occurences:
            words_occurences.append(word_occurences)
    return words_occurences


def find_word_offsets_in_text(word: str, text: str) -> list[int]:
    offsets = []
    start = 0
    while True:
        offset = text.find(word, start)
        if offset == -1:
            break
        offsets.append(offset)
        start = offset + len(word)
    return offsets
