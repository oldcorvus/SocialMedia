
from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
	path('register/', views.UserRegisterView.as_view(), name='user_register'),
	path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
	path('login/', views.UserLoginView.as_view(), name='user_login'),
	path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<slug:user>/',views.UserDetailView.as_view(),name="user_profile"),
    path('profile/<int:pk>/edit/',views.UserUpdateView.as_view(),name="profile_edit"),

]