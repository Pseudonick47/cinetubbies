from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsSelfOrReadOnly(BasePermission):

  def has_permission(self, request, view):
    return True

  def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS:
      return True
    return obj.id == request.user.id
