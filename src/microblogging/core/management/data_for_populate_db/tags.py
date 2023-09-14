from __future__ import annotations

from core.models import Tags

from .provider import WordProvider


class WordGenerate:
    def __init__(self) -> None:
        self.word_generate = WordProvider()
        self.words: set[str] = set()

    def __call__(self, word_count: int) -> list[str]:
        for i in range(word_count):
            word = self.word_generate()
            self.words.add(word.lower())

        return list(self.words)


class PopulateTagsRecord:
    def __init__(self) -> None:
        self.tags_generate = WordGenerate()

    def __call__(self, value_count: int) -> list[Tags]:
        tags_list = []

        value_count *= 5
        words = self.tags_generate(word_count=value_count)
        for word in words:
            tags_list.append(Tags(tag=word))

        tags: list[Tags] = Tags.objects.bulk_create(tags_list)

        return tags
