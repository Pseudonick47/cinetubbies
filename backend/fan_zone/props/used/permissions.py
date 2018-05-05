from rest_framework.permissions import BasePermission


class IsOwner(BaseException):

  def has_object_permission(self, request, view, obj):
    if request.user.is_system_admin():
      return True

    if not request.user.is_user():
      return False

    return request.user.id == obj.owner.id
