from .views import UserViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token


current_user = UserViewSet.as_view({
  'get': 'current_user',
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

urlpatterns = format_suffix_patterns([
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('users/', user_list, name='user-list'),
    path('me/', current_user, name='user-current'),
    path('login/', obtain_jwt_token, name='login'),
    # path('register/', nesto, name='register'),
    # path('logout/', nesto, name='logout'),
])
