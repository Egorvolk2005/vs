from __future__ import annotations

from typing import TYPE_CHECKING, Any

from core.management.data_for_populate_db import (
    PopulateFollowersRecord,
    PopulateLikesRecord,
    PopulateNotificationsRecord,
    PopulateProfileRecord,
    PopulateRepostsRecord,
    PopulateTagsRecord,
    PopulateTwitsRecord,
)
from core.models import Profiles
from django.core.management.base import BaseCommand

if TYPE_CHECKING:
    from django.core.management.base import CommandParser


class Command(BaseCommand):
    def __init__(self) -> None:
        self.tags = PopulateTagsRecord()
        self.profiles = PopulateProfileRecord()
        self.followers = PopulateFollowersRecord()
        self.twits = PopulateTwitsRecord()
        self.likes = PopulateLikesRecord()
        self.reposts = PopulateRepostsRecord()
        self.notifications = PopulateNotificationsRecord()

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("value", nargs="+", type=int)

    def handle(self, *args: tuple[Any, ...], **options: dict[Any, Any]) -> None:
        if Profiles.objects.all():
            return None

        if options["value"]:
            value = options["value"][0]
        else:
            value = 100

        tags = self.tags(value_count=value)

        profiles = self.profiles(value_count=value)

        twits = self.twits(value_count=value, profiles=profiles, tags=tags)

        likes = self.likes(profiles=profiles, twits=twits, max_value=value)

        self.reposts(profiles=profiles, twits=twits, max_value=value)

        self.notifications(notifications=likes)

        self.followers(profiles=profiles, max_value=value)

        return None
