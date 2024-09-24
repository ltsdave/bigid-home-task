import pytest

from app.text_proccesors.find_words import find_word_offsets_in_text


@pytest.mark.parametrize(
    ("word", "text", "expected_offsets"),
    [
        ("hello", "hello hello hello", [0, 6, 12]),
        ("hello", "", []),
        ("hello", "no hello here", [3]),
        ("hello", "now this word is really not here", []),
        ("goodbye", "good", []),
    ],
)
def test_find_word_offsets_in_text(word: str, text: str, expected_offsets: list[int]) -> None:
    offsets = find_word_offsets_in_text(word, text)
    assert offsets == expected_offsets
