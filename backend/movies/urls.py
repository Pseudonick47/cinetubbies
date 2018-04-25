from .views import MovieViewSet
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


movie_detail = MovieViewSet.as_view({
  'get': 'retrieve',
  'put': 'update',
  'patch': 'partial_update',
  'delete': 'destroy'
})

movie_list = MovieViewSet.as_view({
  'get': 'list',
  'post': 'create'
})

urlpatterns = format_suffix_patterns([
  path('<int:pk>/', movie_detail, name='movie-detail'),
  path('', movie_list, name='movie-list')
])
