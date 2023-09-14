from __future__ import annotations

from random import choice, randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Profiles, Twits


class PopulateLikesRecord:
    def __call__(
        self, profiles: list[Profiles], twits: list[Twits], max_value: int
    ) -> list[tuple[Profiles, Twits]]:
        notification_list: list[tuple[Profiles, Twits]] = []
        number_followers = max_value // 10 + max_value % 10
        for twit in twits:
            likes: list[Profiles] = []
            for _ in range(randint(1, number_followers)):
                profile = choice(profiles)
                if profile != twit.profile:
                    likes.append(profile)
                    notification_list.append((profile, twit))
            twit.like.set(likes)

        return notification_list
