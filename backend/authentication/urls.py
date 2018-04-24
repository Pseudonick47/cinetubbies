
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token

from .views import UserViewSet, AdminViewSet


active = UserViewSet.as_view({
  'get': 'active_user',
})

register = UserViewSet.as_view({
  'post': 'register',
})

user = UserViewSet.as_view({
  'get': 'retrieve',
  'put': 'update',
  'patch': 'partial_update',
  'delete': 'destroy',
})

users = UserViewSet.as_view({
  'get': 'list',
})

admins = AdminViewSet.as_view({
  'post': 'create',
  'get': 'list',
})

admin_count = AdminViewSet.as_view({
  'get': 'count'
})

urlpatterns = format_suffix_patterns([
  path('users/<int:pk>/', user, name='user'),
  path('users/', users, name='users'),
  path('auth/me/', active, name='active-user'),
  path('auth/login/', obtain_jwt_token, name='login'),
  path('auth/register/', register, name='register'),
  path('admins/', admins, name='admins'),
  path('admins/count/', admin_count, name='admin-count'),
])
