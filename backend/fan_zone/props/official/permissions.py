from rest_framework.permissions import BasePermission

from authentication.models import FanZoneAdmin


class IsResponsible(BasePermission):

  def has_object_permission(self, request, view, obj):
    if request.user.is_system_admin():
      return True
    admin = FanZoneAdmin.objects.get(id=request.user.id)
    return admin.theater == obj.theater
