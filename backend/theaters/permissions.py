from rest_framework.permissions import BasePermission

from authentication.models import TheaterAdmin


class IsResponsibleForTheater(BasePermission):

  def has_object_permission(self, request, view, obj):
    if request.user.is_system_admin():
      return True
    admin = TheaterAdmin.objects.get(id=request.user.id)
    return admin.theater == obj
