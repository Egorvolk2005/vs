from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Profiles, Twits


class PopulateNotificationsRecord:
    def __call__(self, notifications: list[tuple[Profiles, Twits]]) -> None:
        for profile, twit in notifications:
            profile.notification.add(twit)

        return None
