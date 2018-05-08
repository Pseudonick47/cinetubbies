from rest_framework import permissions
from authentication.models import TheaterAdmin
from sale_tickets.models import TicketOnSale

class IsThisTheaterAdminOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    return request.user.is_theater_admin()

  def has_object_permission(self, request, view, obj):
    admin = TheaterAdmin.objects.get(id=request.user.id)
    ticket = TicketOnSale.objects.get(id=obj.id)
    return admin.theater_id == ticket.theater_id

class IsSelfOrReadOnly(permissions.BasePermission):

  def has_permission(self, request, view):
    return True

  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.user_id == request.user.id
