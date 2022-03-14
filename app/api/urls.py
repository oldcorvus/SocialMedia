from django.urls import path
from rest_framework import routers
from api import views


app_name = 'api'
router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, basename='users')


urlpatterns = [
    path('followers/', views.UserFollowersListView.as_view(), name='followers'),
    path('followings/', views.UserFollowingsListView.as_view(), name='followings'),
]
urlpatterns += router.urls
