from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Profiles, Twits


def add_repost_twits(twit: Twits, profile: Profiles) -> None:
    twit.repost.add(profile)
    return None


def delete_repost_twits(twit: Twits, profile: Profiles) -> None:
    twit.repost.remove(profile)
    return None
