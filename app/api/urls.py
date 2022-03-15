from django.urls import path
from rest_framework import routers
from api.views import user_views, relations_views, blog_views, bookmark_views, comment_views


app_name = 'api'
router = routers.SimpleRouter()
router.register(r'users', user_views.UserViewSet, basename='users')
router.register(r'articles', blog_views.ArticleViewSet, basename='articles')
router.register(r'category', blog_views.CategoryViewSet, basename='category')
router.register(r'bookmark', bookmark_views.BookmarkViewSet,
                basename='bookmark')
router.register(r'comment', comment_views.CommentViewSet,
                basename='comment')

urlpatterns = [
    path('followers/', user_views.UserFollowersListView.as_view(), name='followers'),
    path('followings/', user_views.UserFollowingsListView.as_view(), name='followings'),
    path('articles/active-category/<int:id>/', blog_views.ArticleCategoryListView.as_view(),
         name='active-category'),
    path('category/child-category/<int:id>',
         blog_views.NestedCategoryListView.as_view(), name="category-child"),
    path('articles/like/<int:pk>/<str:action>/',
         blog_views.ArticleLikeView.as_view(), name='like-article'),
    path('articles/user-liked/<int:pk>/', blog_views.ArticleUserLikedListView.as_view(),
         name='user-liked-article'),
    path('bookmark/like/<int:pk>/<str:action>/',
         bookmark_views.BookmarkLikeView.as_view(), name='like-bookmark'),
    path('bookmark/user-liked/<int:pk>/', bookmark_views.BookmarkUserLikedListView.as_view(),
         name='user-liked-bookmark'),
    path('comment/replys/<int:pk>/', comment_views.ReplyOfCommentListView.as_view(),
         name='reply-of-comment'),
    path('comment/create/<str:type>/<int:id>/', comment_views.AddCommentView.as_view(),
         name='add-comment'),
    path('comment/create/<str:type>/<int:id>/<int:reply>/', comment_views.AddCommentView.as_view(),
         name='add-reply'),
    path('relations/following-actions/', relations_views.UserActionsListView.as_view(),
         name='following-actions'),
    path('relations/follow/', relations_views.FollowView.as_view(),
         name='follow'),
    path('relations/unfollow/', relations_views.UnFollowView.as_view(),
         name='unfollow'),
]
urlpatterns += router.urls
