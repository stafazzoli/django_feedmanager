from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission to only allow user/owner of a userpost to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
