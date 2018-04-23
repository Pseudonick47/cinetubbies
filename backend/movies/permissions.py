from rest_framework import permissions

class IsSelfOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.role == 'cinema_admin':
            return True
    
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.admin_id