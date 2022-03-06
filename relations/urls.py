from django.urls import path
from relations.views import FollowView

app_name = "relations"
urlpatterns = [
    path('users/follow/', FollowView.as_view(), name='user_follow'),
]
