#emall/user/rbac.py
from rest_framework import permissions


# Check for django staff user permissions
class IsManager(permissions.BasePermission):

    """
    Return True, if request user scope is "MANAGER", otherwise return False
    """
    def has_permission(self, request, view):
        try:
            user_scope = request.user.user_scope
            if user_scope == "MANAGER":
                return True
            else:
                return False
        except Exception as ex:
            return False
        

class IsAdmin(permissions.BasePermission):

    """
    Return True, if request user scope is "MANAGER", otherwise return False
    """
    def has_permission(self, request, view):
        try:
            user_scope = request.user.user_scope
            if user_scope == "ADMIN":
                return True
            else:
                return False
        except Exception as ex:
            return False
        

class IsGetOrAdmin(permissions.BasePermission):

    """
    Return True, if request user scope is "MANAGER", otherwise return False
    """
    def has_permission(self, request, view):
        try:
            # Check if request method is GET
            if request.method == "GET":
                return True
            
            if request.user and request.user.is_authenticated:
                user_scope = request.user.user_scope
                if user_scope == "ADMIN":
                    return True
            return False
        
        except Exception as ex:
            return False