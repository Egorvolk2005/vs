from __future__ import annotations

from typing import TYPE_CHECKING

from core.bussiness_logic.exeptions import GetValueError
from core.bussiness_logic.servises import (
    add_repost_twits,
    delete_repost_twits,
    get_twit_by_id,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from core.models import Twits
    from django.http import HttpRequest, HttpResponse


@login_required()
@require_http_methods(["GET"])
def repost_twits_controller(request: HttpRequest, twit_id: int) -> HttpResponse:
    try:
        operation = request.GET["operation"]
    except MultiValueDictKeyError:
        return HttpResponseBadRequest(content="Invalid request")

    twit: Twits = get_twit_by_id(twit_id=twit_id)
    if twit.profile == request.user:
        return redirect(to="index")

    if operation == "add":
        try:
            add_repost_twits(twit=twit, profile=request.user)
        except GetValueError:
            return HttpResponseBadRequest(content="Twit does not exist")

    elif operation == "delete":
        try:
            delete_repost_twits(twit=twit, profile=request.user)
        except GetValueError:
            return HttpResponseBadRequest(content="Twit does not exist")

    else:
        return HttpResponseBadRequest(content="Incorrect operation")

    return redirect(to="view_twit", twit_id=twit_id)
