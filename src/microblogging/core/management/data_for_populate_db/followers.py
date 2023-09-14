from __future__ import annotations

from random import choice, randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Profiles


class PopulateFollowersRecord:
    def __call__(self, profiles: list[Profiles], max_value: int) -> None:
        number_followers = max_value // 10 + max_value % 10
        for profile in profiles:
            followers: list[Profiles] = []
            for _ in range(randint(1, number_followers)):
                follower = choice(profiles)
                if follower != profile:
                    followers.append(choice(profiles))

            profile.followers.set(followers)
        return None
