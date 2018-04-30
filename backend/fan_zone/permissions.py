from rest_framework.permissions import BasePermission


class IsResponsibleForOfficialProp(BasePermission):

  def has_object_permission(self, request, view, obj):
    if request.user.is_system_admin():
      return True
    return request.user.theater == obj.theater
