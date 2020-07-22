from rest_framework.permissions import BasePermission

# Application imports
from templates.error_template import ErrorTemplate

class IsAdmin(BasePermission):
    message = ErrorTemplate.AuthorizedError.ADMIN_REQUIRED

    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_active

class IsUser(BasePermission):
    message = ErrorTemplate.AuthorizedError.USER_REQUIRED

    def has_permission(self, request, view):
        return request.user.is_active 
