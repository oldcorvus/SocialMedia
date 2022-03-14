from django.urls import path
from .views import ArticleUpdateView, IndexPage, ArticleCreateView, ArticleDeleteView, ArticleLikeView, ArticleListView, ArticleDetailView, UserArticlesListView
ArticleListView, ArticleUpdateView, UserArticlesListView

app_name = "blog"
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('category/<str:slug>/', ArticleListView.as_view(), name='category'),
    path('articles/<int:year>/<int:month>/<int:day>/<str:slug>/',
         ArticleDetailView.as_view(), name='article_detail'),
    path('aricles/create/', ArticleCreateView.as_view(), name='add-article'),
    path('articles/<str:username>/',
         UserArticlesListView.as_view(), name='user-articles'),
    path('articles/edit/<int:pk>/',
         ArticleUpdateView.as_view(), name='article-edit'),
    path('articles/delete/<int:pk>/',
         ArticleDeleteView.as_view(), name='article-delete'),
    path('article/like/', ArticleLikeView.as_view(), name='like'),
]
