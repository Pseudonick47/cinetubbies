from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import TheaterAPI


theater = TheaterAPI.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'update',
    'delete': 'destroy',
})


theaters = TheaterAPI.as_view({
    'get': 'list',
    'post': 'create',
})

update_admin = TheaterAPI.as_view({
    'put': 'update_admin',
    'patch': 'update_admin'
})


urlpatterns = format_suffix_patterns([
    path('', theaters, name='theaters'),
    path('<int:pk>', theater, name='theater'),
    path('<int:pk>/admin', update_admin, name='update_admin')
])
