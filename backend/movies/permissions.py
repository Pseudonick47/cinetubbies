from rest_framework import permissions
from authentication.models import TheaterAdmin

class IsCreatorOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    if request.user.role == 'cinema_admin':
      return True

  def has_object_permission(self, request, view, obj):
    admin = TheaterAdmin.objects.get(user_ptr_id=request.user.id)
    return admin.theater_id == obj.theater_id