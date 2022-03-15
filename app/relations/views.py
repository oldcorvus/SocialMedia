
from django.http import JsonResponse
from .models import Contact
from relations.utils import create_action
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from blog.mixins import AjaxRequiredMixin
User = get_user_model()


class FollowView(LoginRequiredMixin, AjaxRequiredMixin, View):

    def post(self, request):
        user_id = request.POST.get('id')
        action = request.POST.get('action')
        if user_id and action:
            try:

                user = User.objects.get(id=user_id)
                if action == 'follow':
                    request.user.following.add(user)
                    create_action(request.user, 'is following', user)
                else:
                    self.request.user.following.remove(user)

                return JsonResponse({'status': 'ok'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'error'})
        return JsonResponse({'status': 'error'})

