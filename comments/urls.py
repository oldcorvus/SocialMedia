from django.urls import path
from .views import *

app_name = "comment"
urlpatterns = [

    path('comments/<str:type>/<int:id>/',
         CommentCreateView.as_view(), name='add-comment'),
    path('comments/<str:type>/<int:id>/<int:reply>',
         CommentCreateView.as_view(), name='add-reply'),
    path('comments/approve/<int:id>',
         ApproveComment.as_view(), name='approve-comment'),

]
