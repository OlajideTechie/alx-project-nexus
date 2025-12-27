from rest_framework.permissions import BasePermission

""" 
Custom permission classes for user roles."""
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated 
                and request.user.is_staff
        )
