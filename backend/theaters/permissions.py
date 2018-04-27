from rest_framework.permissions import BasePermission

from authentication.models import SYSTEM_ADMIN, THEATER_ADMIN


class IsResponsibleForTheater(BasePermission):

  def has_object_permission(self, request, view, obj):
    return request.user.id in [admin.id for admin in obj.admins.all()] or \
           request.user.role == SYSTEM_ADMIN[0]

class IsTheaterOrSystemAdmin(BasePermission):
  def has_permission(self, request, view):
    return request.user.role == SYSTEM_ADMIN[0] or \
           request.user.role == THEATER_ADMIN[0]

class IsSystemAdmin(BasePermission):

  def has_permission(self, request, view):
    return request.user.role == 'admin'
