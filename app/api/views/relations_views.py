
from django.shortcuts import get_object_or_404
from api.permissions import IsAuthorOrReadOnly
from relations.models import Action, Contact
from relations.seriliazers import ActionSerializer, ConatctSerializer
from comments.models import Comment
from rest_framework import generics, permissions,  viewsets, status
from relations.utils import create_action
from django.contrib.auth import get_user_model
from comments.seriliazers import CommentSerializer
from bookmark.models import ImageBookmark
from blog.models import Article
from rest_framework import viewsets, mixins
from api.pagination import ActionLimitOffsetPagination
from rest_framework.response import Response
User = get_user_model()


class UserActionsListView(generics.ListAPIView):
    """List of all following users actions for a user"""
    serializer_class = ActionSerializer
    pagination_class = ActionLimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        print(self.request.user)

        following_ids = self.request.user.following.values_list('id',
                                                                flat=True)
        actions = Action.objects.exclude(
            user=self.request.user).filter(user_id__in=following_ids)
        return actions


class FollowView(generics.CreateAPIView):
    """follow user """
    serializer_class = ConatctSerializer
    queryset = Contact.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        user_id = self.request.POST.get('user_to')
        if user_id:
            user = User.objects.get(id=user_id)
            contact = self.request.user.following.add(user)
            create_action(self.request.user, 'is following', user)
        return contact


class UnFollowView(generics.CreateAPIView):
    """unfollow user """
    serializer_class = ConatctSerializer
    queryset = Contact.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        user_id = self.request.POST.get('user_to')
        if user_id:
            user = User.objects.get(id=user_id)
            contact = self.request.user.following.remove(user)
            create_action(self.request.user, 'unfollowed', user)
        return contact
