from rest_framework import permissions
from authentication.models import TheaterAdmin
from movies.models import Movie

class IsThisTheaterAdminOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    return request.user.is_theater_admin()

  def has_object_permission(self, request, view, obj):
    admin = TheaterAdmin.objects.get(id=request.user.id)
    movie = Movie.objects.get(id=obj.movie_id)
    return admin.theater_id == movie.theater_id
    