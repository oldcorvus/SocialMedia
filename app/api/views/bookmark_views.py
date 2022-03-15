
from django.shortcuts import get_object_or_404
from account.serializers import UserSerializer
from api.permissions import  IsAuthorOrReadOnly, IsOwner
from rest_framework import generics, permissions, status, viewsets
from relations.utils import create_action
from django.contrib.auth import get_user_model
from bookmark.seriliazers import BookmarkSerializer
from rest_framework.response import Response
from api.pagination import BookmarkLimitOffsetPagination
from bookmark.models import ImageBookmark
User = get_user_model()


class BookmarkViewSet(viewsets.ModelViewSet):
    """create, update, delete, retrive and list  Bookmarks"""

    queryset = ImageBookmark.objects.all()
    serializer_class = BookmarkSerializer
    filterset_fields = ['author__username', 'created']
    search_fields = ['title', 'url', 'author__username']
    ordering_fields = ['created']

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
        bookmark = serializer.save(author=author)
        create_action(self.request.user, 'posted  bookmark', bookmark)

    def perform_update(self, serializer):
        author = self.request.user
        bookmark = serializer.save(author=author)
        create_action(self.request.user, 'edited  bookmark', bookmark)


class BookmarkUserLikedListView(generics.ListAPIView):
    """List of all users liked  bookmark"""
    serializer_class = UserSerializer
    pagination_class = BookmarkLimitOffsetPagination

    def get_queryset(self):
        bookmark_id = self.kwargs.get('pk')
        return get_object_or_404(ImageBookmark, pk=bookmark_id).users_like.all()


class BookmarkLikeView(generics.UpdateAPIView):
    """Like bookmark """
    serializer_class = BookmarkSerializer
    queryset = ImageBookmark.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        bookmark_id = self.kwargs.get('pk')
        action = self.kwargs.get('action')
        if bookmark_id and action:
            bookmark = get_object_or_404(ImageBookmark, pk=bookmark_id)
            if action == 'like':
                create_action(self.request.user, 'likes', bookmark)
                bookmark.users_like.add(self.request.user)
            else:
                create_action(self.request.user, 'dislikes', bookmark)
                bookmark.users_like.remove(self.request.user)

            return Response(self.get_serializer(bookmark).data)
        else:
            return Response({'error': 'not allowed'}, status=status.HTTP_400_BAD_REQUEST)
