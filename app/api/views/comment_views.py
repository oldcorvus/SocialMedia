
from django.shortcuts import get_object_or_404
from api.permissions import IsAuthorOrReadOnly
from comments.models import Comment
from rest_framework import generics, permissions,  viewsets, status
from relations.utils import create_action
from django.contrib.auth import get_user_model
from comments.seriliazers import CommentSerializer
from bookmark.models import ImageBookmark
from blog.models import Article
from rest_framework import viewsets, mixins
from api.pagination import CommentLimitOffsetPagination
from rest_framework.response import Response
User = get_user_model()


class CommentViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """update, delete, retrive and list  comments"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = ['author__username', 'created', 'is_reply', ]
    search_fields = ['author__username', 'body']
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

        if self.kwargs.get('type') == 'article':
            target = get_object_or_404(Article, pk=self.kwargs.get('id'))
        else:
            target = get_object_or_404(ImageBookmark, pk=self.kwargs.get('id'))

        comment = serializer.save(author=author, content_object=target)

        create_action(self.request.user, 'posted  comment', comment)

    def perform_update(self, serializer):
        author = self.request.user
        comment = serializer.save(author=author)
        create_action(self.request.user, 'edited  comment', comment)


class ReplyOfCommentListView(generics.ListAPIView):
    """List of all replys for a comment"""
    serializer_class = CommentSerializer
    pagination_class = CommentLimitOffsetPagination

    def get_queryset(self):
        comment_id = self.kwargs.get('pk')
        return get_object_or_404(Comment, pk=comment_id).reply_comment.all()


class AddCommentView(generics.CreateAPIView):
    """add comment or reply """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        if self.kwargs.get('type') == 'article':
            target = get_object_or_404(Article, pk=self.kwargs.get('id'))
        else:
            target = get_object_or_404(ImageBookmark, pk=self.kwargs.get('id'))

        serializer.save(author=self.request.user, content_object=target, )
        if self.kwargs.get('reply'):
            serializer.save(is_reply=True, reply=get_object_or_404(
                Comment, pk=self.kwargs['reply']))
