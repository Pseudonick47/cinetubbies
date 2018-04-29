from rest_framework.permissions import BasePermission

from authentication.models import SYSTEM_ADMIN, THEATER_ADMIN


class IsResponsibleForTheater(BasePermission):

  def has_object_permission(self, request, view, obj):
    return request.user.id in [admin.id for admin in obj.admins.all()] or \
           request.user.is_system_admin()

