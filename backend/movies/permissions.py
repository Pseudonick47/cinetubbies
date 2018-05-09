from rest_framework import permissions
from authentication.models import TheaterAdmin

class IsThisTheaterAdminOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    return request.user.is_theater_admin()

  def has_object_permission(self, request, view, obj):
    admin = TheaterAdmin.objects.get(id=request.user.id)
    return admin.theater_id == obj.theater_id
    