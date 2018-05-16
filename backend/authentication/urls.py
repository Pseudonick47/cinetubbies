from django.urls import include
from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from fan_zone.reservations.urls import urls_by_user as prop_reservation_urls

from .views import AdminViewSet
from .views import UserViewSet
from .views import FriendViewSet
from .views import SystemAdminViewSet


active = UserViewSet.as_view({
  'get': 'active_user',
})

register = UserViewSet.as_view({
  'post': 'create',
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

admins = SystemAdminViewSet.as_view({
  'post': 'create',
  'get': 'list',
})

admin_count = SystemAdminViewSet.as_view({
  'get': 'count'
})

admin_theater = AdminViewSet.as_view({
  'get': 'get_theater'
})

user_friends = FriendViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'delete': 'delete',
})

search_friends = FriendViewSet.as_view({
    'get': 'search_for_friends'
})

urlpatterns = [
  path('users/<int:pk>/friends/', user_friends, name='user-friends'),
  path('users/friends/<str:query>', search_friends, name='user-friends-search'),
  path('users/<int:pk>/', user, name='user'),
  path('users/<int:user_id>/reservations/', include(prop_reservation_urls), name='user-prop-reservations'),
  path('users/<int:user_id>/props/', include('fan_zone.props.used.urls'), name='user-props'),
  path('users/', users, name='users'),
  path('auth/me/', active, name='active-user'),
  path('auth/login/', obtain_jwt_token, name='login'),
  path('auth/register/', register, name='register'),
  path('admins/', admins, name='admins'),
  path('admins/count', admin_count, name='admin-count'),
  path('admins/<int:pk>/theater', admin_theater, name='admin-theater'),
]
