
from django.shortcuts import get_object_or_404
from account.serializers import UserSerializer
from api.permissions import IsAdmin, IsAuthorOrReadOnly, IsOwner
from rest_framework import generics, permissions, status, viewsets
from relations.utils import create_action
from django.contrib.auth import get_user_model
from blog.models import Article, Category
from blog.seriliazers import ArticleSerializer, CategorySerializer
from rest_framework.response import Response
from api.pagination import ArticleLimitOffsetPagination
User = get_user_model()


class ArticleViewSet(viewsets.ModelViewSet):
    """create, update, delete, retrive and list  articles"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filterset_fields = ['status', 'publish']
    search_fields = ['title', 'content']
    ordering_fields = ['publish']

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy', 'retrieve']:
            permission_classes = [
                permissions.IsAuthenticated, IsAuthorOrReadOnly]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, ]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        author = self.request.user
        article = serializer.save(author=author)
        create_action(self.request.user, 'posted  article', article)

    def perform_update(self, serializer):
        author = self.request.user
        article = serializer.save(author=author)
        create_action(self.request.user, 'edited  article', article)


class CategoryViewSet(viewsets.ModelViewSet):
    """create, update, delete, retrive and list  category"""

    queryset = Category.objects.active()
    serializer_class = CategorySerializer
    filterset_fields = ['status', ]
    search_fields = ['title', 'description']
    ordering_fields = ['publish']

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy', 'create']:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]


class ArticleCategoryListView(generics.ListAPIView):
    """List of all active article category"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        article = self.kwargs.get('id')
        return get_object_or_404(Article, pk=article).active_categories()


class NestedCategoryListView(generics.ListAPIView):
    """List of all  category child"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('id'))
        return Category.objects.filter(parent=category)


class ArticleUserLikedListView(generics.ListAPIView):
    """List of all users liked article """
    serializer_class = UserSerializer
    pagination_class = ArticleLimitOffsetPagination

    def get_queryset(self):
        article = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=article).users_like.all()


class ArticleLikeView(generics.UpdateAPIView):
    """Like article """
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        article_id = self.kwargs.get('pk')
        action = self.kwargs.get('action')
        if article_id and action:
            article = get_object_or_404(Article, pk=article_id)
            if action == 'like':
                create_action(self.request.user, 'likes', article)
                article.users_like.add(self.request.user)
            else:
                create_action(self.request.user, 'dislikes', article)
                article.users_like.remove(self.request.user)

            return Response(self.get_serializer(article).data)
        else:
            return Response({'error': 'not allowed'}, status=status.HTTP_400_BAD_REQUEST)
