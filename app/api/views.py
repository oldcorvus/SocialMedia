
from django.shortcuts import get_object_or_404
from account.serializers import UserSerializer
from api.permissions import IsOwner
from rest_framework import generics, permissions, status
from django.http import JsonResponse
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.response import Response
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated, IsOwner]

        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]


class UserFollowersListView(generics.ListAPIView):
    """List of all user followers"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return get_object_or_404(User, pk=user.id).following.followers.all()


class UserFollowingsListView(generics.ListAPIView):
    """List of all user followers"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return get_object_or_404(User, pk=user.id).following
