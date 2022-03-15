from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a post
        return obj.author == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is owner of the object. 
    """
    message = "You dont have permission"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to check if the user is admin. 
    """
    message = "You dont have permission .only admins can create new category"

    def has_permission(self, request, view):

        return request.user.is_admin
