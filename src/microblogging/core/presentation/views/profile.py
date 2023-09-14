from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import (
    CreateUniqueError,
    GetValueError,
    PaginationError,
)
from core.bussiness_logic.servises import (
    add_follow,
    edit_profile,
    get_followers,
    get_following,
    get_profile_in_follow,
    get_twits,
    get_twits_reposts,
    get_user_profile,
    parsing_create_unique_error_message,
    remove_follow,
)
from core.presentation.common import get_edit_form
from core.presentation.paginator import CustomPaginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@login_required()
@require_http_methods(["GET"])
def profile_users_controller(request: HttpRequest, username: str) -> HttpResponse:
    try:
        page_num = request.GET["page"]
    except KeyError:
        page_num = 1

    try:
        profile = get_user_profile(username=username)
    except GetValueError:
        return redirect(to="index")

    repost_twits = get_twits_reposts(profile=profile)

    twits = get_twits(twits_list=repost_twits, profile=profile)

    paginator = CustomPaginator(max_value=20)
    try:
        twits_paginator = paginator.paginate(data=twits, page_num=page_num)
    except PaginationError:
        return HttpResponseBadRequest(
            content="Page with provided number doesn't exist."
        )

    context = {"title": "Profile", "profile": profile, "twits": twits_paginator}

    if request.user.username == username:
        return render(request=request, template_name="profile.html", context=context)

    follow = get_profile_in_follow(profile=request.user, profile_follow=profile)
    context.update({"follow": follow})

    return render(request=request, template_name="profile_users.html", context=context)


@login_required()
@require_http_methods(["GET"])
def profile_following_controller(request: HttpRequest, username: str) -> HttpResponse:
    following = get_following(username=username)
    context = {"title": "Following", "following": following}
    return render(
        request=request, template_name="profile_followings.html", context=context
    )


@login_required()
@require_http_methods(["GET"])
def profile_followers_controller(request: HttpRequest, username: str) -> HttpResponse:
    followers = get_followers(username=username)
    context = {"title": "Followers", "followers": followers}
    return render(
        request=request, template_name="profile_followers.html", context=context
    )


@login_required()
@require_http_methods(["GET"])
def profile_edit_controller(request: HttpRequest) -> HttpResponse:
    context = {"title": "Edit profile"}
    return render(request=request, template_name="edit_profile.html", context=context)


@login_required()
@require_http_methods(["GET", "POST"])
def edit_field_profile_controller(request: HttpRequest, field: str) -> HttpResponse:
    context = {"title": "Edit field"}
    try:
        initial = {field: getattr(request.user, field)}
    except AttributeError:
        return HttpResponseBadRequest(content="Invalid edit request")

    try:
        form = get_edit_form(field=field, initial=initial)
    except GetValueError:
        HttpResponseBadRequest(content="Invalid edit request")

    if request.POST:
        form = get_edit_form(
            field=field, data=request.POST, files=request.FILES, initial=initial
        )
        if form.has_changed():
            if form.is_valid():
                try:
                    data = form.cleaned_data
                    edit_profile(
                        username=request.user.username,
                        data=data,
                        files=request.FILES,
                    )
                    return redirect(to="edit_profile")

                except CreateUniqueError as err:
                    field = parsing_create_unique_error_message(err=err)
                    form.add_error(field=field, error=f"{field} already exists")
        else:
            redirect(to="edit_profile")

    context.update({"form": form})
    return render(
        request=request, template_name="edit_field_profile.html", context=context
    )


@login_required()
@require_http_methods(["GET"])
def follow_profile_controller(request: HttpRequest, username: str) -> HttpResponse:
    try:
        operation = request.GET["operation"]
    except MultiValueDictKeyError:
        return HttpResponseBadRequest(content="Invalid request")

    if username != request.user.username:
        if operation == "add":
            try:
                add_follow(user=request.user, user_following=username)
            except GetValueError:
                return HttpResponseBadRequest(content="User does not exist")

        elif operation == "remove":
            try:
                remove_follow(user=request.user, user_following=username)
            except GetValueError:
                return HttpResponseBadRequest(content="User does not exist")

        else:
            return HttpResponseBadRequest(content="Incorrect operation")

    return redirect(to="profile_users", username=username)
