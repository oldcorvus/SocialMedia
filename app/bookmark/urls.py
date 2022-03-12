from django.urls import path
from .views import BookmarkDeleteView, BookmarkUpdateView, BookmarkLikeView, BookmarkListView, BookmarkDetailView, BookmarkCreateView

app_name = 'bookmark'

urlpatterns = [
    path('bookmark/create/', BookmarkCreateView.as_view(), name='create'),
    path('bookmark/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:id>/',
         BookmarkDetailView.as_view(), name='detail'),
    path('bookmark/edit/<int:pk>/',
         BookmarkUpdateView.as_view(), name='bookmark-edit'),
    path('bookmark/delete/<int:pk>/',
         BookmarkDeleteView.as_view(), name='bookmark-delete'),
    path('bookmark/like/', BookmarkLikeView.as_view(), name='like'),
    path('bookmark/list/', BookmarkListView.as_view(), name='list'),
]
