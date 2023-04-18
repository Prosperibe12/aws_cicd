from rest_framework.permissions import BasePermission


class IsActiveAuthenticated(BasePermission):
    '''
    Define Our own Custom Permission for
    Active and Authenticated Users only
    '''
    def has_permission(self, request, view):
        return bool(
         request.user and request.user.is_authenticated
         and request.user.is_active
        )
