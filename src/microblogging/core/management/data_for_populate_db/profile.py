from __future__ import annotations

from datetime import datetime
from random import randint
from uuid import uuid4

from core.models import Profiles
from django.contrib.auth.hashers import make_password

from .dto import ProfilePopulateDTO
from .provider import CountryProvider, NameProvider, SurnameProvider
from .tags import WordGenerate


class ProfileGenerate:
    def __init__(self) -> None:
        self.name_generate = NameProvider()
        self.surname_generate = SurnameProvider()
        self.word_generate = WordGenerate()
        self.country_generate = CountryProvider()

    def __call__(self, value_count: int) -> list[ProfilePopulateDTO]:
        profile_list: list[ProfilePopulateDTO] = []

        for i in range(value_count):
            password = make_password("123456")
            name = self.name_generate()
            surname = self.surname_generate()
            description = " ".join(self.word_generate(word_count=randint(5, 15)))
            date_of_birth = datetime(
                year=randint(1968, 2004), month=randint(1, 12), day=randint(1, 28)
            )
            username = name + str(uuid4())[:6]
            email = "www." + username + "@gmail.com"
            country = self.country_generate().lower()

            profile_list.append(
                ProfilePopulateDTO(
                    username=username,
                    first_name=name,
                    last_name=surname,
                    password=password,
                    email=email,
                    country=country,
                    description=description,
                    date_of_birth=date_of_birth,
                )
            )

        return profile_list


class PopulateProfileRecord:
    def __init__(self) -> None:
        self.profiles_ganerate = ProfileGenerate()

    def __call__(self, value_count: int) -> list[Profiles]:
        profiles_list: list[ProfilePopulateDTO] = self.profiles_ganerate(
            value_count=value_count
        )

        profiles_for_record: list[Profiles] = []

        for profile in profiles_list:
            profiles_for_record.append(
                Profiles(
                    username=profile.username,
                    first_name=profile.first_name,
                    last_name=profile.last_name,
                    email=profile.email,
                    date_of_birth=profile.date_of_birth,
                    country=profile.country,
                    password=profile.password,
                    description=profile.description,
                    is_active=True,
                )
            )

        profiles: list[Profiles] = Profiles.objects.bulk_create(profiles_for_record)

        return profiles
