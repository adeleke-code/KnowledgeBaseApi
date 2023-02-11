from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed







class IsAdmin(permissions.BasePermission):
    # print("Hey I'm here")
    """
    Allows access only to only admin users.
    """
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided oh ")