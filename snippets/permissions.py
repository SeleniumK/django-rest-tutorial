from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of object to edit."""

    def has_object_permission(self, request, view, obj):
        """Check object permissions against the request's user."""
        # Read Permissions are always allowed
        # always allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permissions are only allowed for owner
        return obj.owner == request.user
