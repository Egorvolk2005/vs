from __future__ import annotations

from random import choice, randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Profiles, Twits


class PopulateRepostsRecord:
    def __call__(
        self, profiles: list[Profiles], twits: list[Twits], max_value: int
    ) -> None:
        number_followers = max_value // 10 + max_value % 10
        for twit in twits:
            reposts: list[Profiles] = []
            for _ in range(randint(1, number_followers)):
                profile: Profiles = choice(profiles)
                if profile != twit.profile:
                    reposts.append(profile)

            twit.repost.set(reposts)

        return None
