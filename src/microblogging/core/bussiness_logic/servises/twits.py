from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import GetValueError, ProfileAccessError
from core.models import Twits
from django.db.models import Count, Q

from .tags import get_tags

if TYPE_CHECKING:
    from core.bussiness_logic.dto import TwitsDTO
    from core.models import Profiles, Tags
    from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)


def get_twit_by_id(twit_id: int) -> Twits:
    try:
        twit: Twits = Twits.objects.select_related("profile", "answer_to_twit").get(
            id=twit_id
        )
    except Twits.DoesNotExist:
        raise GetValueError

    return twit

 
def get_twits_reposts(profile: Profiles) -> QuerySet:
    repost_twits = Twits.objects.prefetch_related("repost").filter(repost=profile)
    logger.info(f"Get twits repost. profile: {profile.id}")
    return repost_twits


def get_twits(twits_list: QuerySet, profile: Profiles) -> QuerySet:
    twits = (
        Twits.objects.select_related("profile", "answer_to_twit")
        .prefetch_related("like", "repost")
        .annotate(
            count_like=Count("like", distinct=True),
            count_repost=Count("repost", distinct=True),
            count_answer=Count("answer", distinct=True),
        )
        .filter(Q(profile=profile) | Q(id__in=twits_list))
        .order_by("-created_at")
    )
    logger.info(f"Get twits and repost twits. profile: {profile.id}")
    return twits


def add_twits(data: TwitsDTO, profile: Profiles) -> Twits:
    tags = get_tags(tags=data.tag)

    twit_db: Twits = Twits.objects.create(text=data.text, profile=profile)

    twit_db.tag.set(tags)
    logger.info(f"Create twit. twit: {twit_db.id}")
    return twit_db


def view_twits(twit_id: int) -> tuple[Twits, list[Tags], list[Twits]]:
    try:
        twit: Twits = get_twit_by_id(twit_id=twit_id)
    except Twits.DoesNotExist:
        raise GetValueError

    twits_ansver = Twits.objects.filter(answer_to_twit=twit)

    tag = twit.tag.all()

    logger.info(f"Get info twit. twit: {twit.id}")

    return twit, list(tag), list(twits_ansver)


def delete_twits(twit_id: int, profile: Profiles) -> None:
    twit: Twits = get_twit_by_id(twit_id=twit_id)


    if twit.profile != profile:
        raise ProfileAccessError

    twit.delete()

    return None


def get_profile_like_on_twit(profile: Profiles, twit: Twits) -> bool:
    like_twit: bool = twit.like.filter(pk=profile.pk).exists()
    return like_twit


def get_profile_repost_on_twit(profile: Profiles, twit: Twits) -> bool:
    repost_twit: bool = twit.repost.filter(pk=profile.pk).exists()
    return repost_twit


def creat_answer_to_twit(twit_id: int, data: TwitsDTO, profile: Profiles) -> None:
    twit = get_twit_by_id(twit_id=twit_id)

    tags = get_tags(tags=data.tag)

    twit_answer = Twits.objects.create(
        text=data.text, answer_to_twit=twit, profile=profile
    )

    twit_answer.tag.set(tags)

    return None


def get_info_twit_for_edit(twit_id: int) -> tuple[Twits, list[Tags]]:
    twit: Twits = get_twit_by_id(twit_id=twit_id)

    tags = twit.tag.all()
    return twit, list(tags)


def edit_twit(twit_db: Twits, data: TwitsDTO) -> None:
    twit_db.text = data.text
    twit_db.save()

    tags = get_tags(tags=data.tag)
    twit_db.tag.set(tags)

    return None
