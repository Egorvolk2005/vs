from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Profiles, Twits


def add_like_twits(twit: Twits, profile: Profiles) -> None:
    twit.like.add(profile)
    return None


def delete_like_twits(twit: Twits, profile: Profiles) -> None:
    twit.like.remove(profile)
    return None
