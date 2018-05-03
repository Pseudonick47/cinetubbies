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

get_showtimes = MovieViewSet.as_view({
  'get': 'get_showtimes'
})

rating = MovieViewSet.as_view({
  'post': 'update_rating'
})

urlpatterns = format_suffix_patterns([
  path('<int:pk>/', movie_detail, name='movie-detail'),
  path('', movie_list, name='movie-list'),
  path('<int:pk>/showtimes', get_showtimes, name='get-showtimes'),
  path('rating', rating, name='rating')
])
