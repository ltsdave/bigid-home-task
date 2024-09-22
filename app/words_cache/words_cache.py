from app.types import WordsOccurecnes


class WordsCache:
    def __init__(self):
        self.state = {}

    def update_cache(self, words_occurences: WordsOccurecnes, words_outside_cache: list[str]) -> None:
        for word_occurences in words_occurences:
            self.state.update(word_occurences)
        for word in words_outside_cache:
            if not self.state.get(word):
                self.state[word] = None

    def get_words_outside_cache(self, words: list[str]) -> list[str]:
        words_outside_cache: list[str] = []
        for word in words:
            if word not in self.state:
                words_outside_cache.append(word)
        return words_outside_cache

    def get_words_occurences(self, words: list[str]) -> WordsOccurecnes:
        words_occurences: WordsOccurecnes = []
        for word in words:
            occurences = self.state.get(word)
            if occurences:
                words_occurences.append({word: occurences})
        return words_occurences

    def clear(self) -> None:
        self.state = {}
