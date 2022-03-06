from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseBadRequest

User = get_user_model()

class AuthorMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class AjaxRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return HttpResponseBadRequest()
        return super().dispatch(request, *args, **kwargs)
