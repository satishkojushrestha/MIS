from typing import Any
from django import http
from django.views.generic import View
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from .exceptions import ValidationException


class GenericView(View, ValidationException):

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...

    def head(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...

    def post(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...

    def delete(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...
    
    def put(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...

    def patch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse: ...

    def format_resp(self, **kwargs):
        return kwargs
    
    
class GenericListView(MultipleObjectTemplateResponseMixin, MultipleObjectMixin, GenericView): ...  


class GenericDetailView(SingleObjectTemplateResponseMixin, SingleObjectMixin, GenericView): ...
