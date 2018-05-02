from .views import ShowtimeViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


showtime_detail = ShowtimeViewSet.as_view({
  'get': 'retrieve',
  'put': 'update',
  'delete': 'destroy'
})

showtime_list = ShowtimeViewSet.as_view({
  'post': 'create'
})

urlpatterns = format_suffix_patterns([
  path('<int:pk>/', showtime_detail, name='showtime-detail'),
  path('', showtime_list, name='showtime-list')
])
