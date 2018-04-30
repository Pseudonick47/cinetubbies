from .views import UserViewSet, FriendViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token


current_user = UserViewSet.as_view({
    'get': 'current_user',
})

user_register = UserViewSet.as_view({
    'post': 'create',
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_friends = FriendViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'delete': 'delete',
})

search_friends = FriendViewSet.as_view({
    'get': 'search_for_friends'
})

urlpatterns = format_suffix_patterns([
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('users/<int:pk>/friends/', user_friends, name='user-friends'),
    path('users/friends/<str:query>', search_friends, name='user-friends-search'),
    path('users/', user_list, name='user-list'),
    path('auth/me/', current_user, name='user-current'),
    path('auth/login/', obtain_jwt_token, name='login'),
    path('auth/register/', user_register, name='register'),
])
