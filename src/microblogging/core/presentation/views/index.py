from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET"])
def index_controller(request: HttpRequest) -> HttpResponse:
    context = {"title": "MICROBLOG"}
    return render(request=request, template_name="index.html", context=context)
