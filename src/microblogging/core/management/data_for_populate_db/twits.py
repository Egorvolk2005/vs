from __future__ import annotations

from random import choice, randint

from core.models import Profiles, Tags, Twits

from .tags import WordGenerate


class TwitGenerate:
    def __init__(self) -> None:
        self.word_generate = WordGenerate()

    def __call__(self, value_count: int) -> list[str]:
        twits_text_list: list[str] = []

        for i in range(value_count):
            text = " ".join(self.word_generate(word_count=randint(5, 30)))
            text += choice([" www.djangoproject.com", "", "", ""])
            twits_text_list.append(text)

        return twits_text_list


class PopulateTwitsRecord:
    def __init__(self) -> None:
        self.twits_generate = TwitGenerate()

    def __call__(
        self, value_count: int, profiles: list[Profiles], tags: list[Tags]
    ) -> list[Twits]:
        value_count *= 5
        twits_list_form_db: list[Twits] = []
        twits_text = self.twits_generate(value_count=value_count)

        for text in twits_text:
            profile = choice(profiles)

            if twits_list_form_db:
                answer = choice(
                    [choice(twits_list_form_db), None, None, None, None, None, None]
                )
            else:
                answer = None

            twit = Twits.objects.create(
                text=text, answer_to_twit=answer, profile=profile
            )
            twits_list_form_db.append(twit)

            tags_for_record = []
            for _ in range(randint(1, 20)):
                tags_for_record.append(choice(tags))

            twit.tag.set(tags_for_record)

        return twits_list_form_db
