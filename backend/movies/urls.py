from .views import PublicAPI, RestrictedAPI
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

movie_detail = RestrictedAPI.as_view({
  'get': 'retrieve',
  'put': 'update',
  'delete': 'destroy'
})

movie_list = RestrictedAPI.as_view({
  'get': 'list',
  'post': 'create'
})

get_showtimes = RestrictedAPI.as_view({
  'get': 'get_showtimes'
})

update_rating = PublicAPI.as_view({
  'post': 'update_rating'
})

urlpatterns = format_suffix_patterns([
  path('<int:pk>/', movie_detail, name='movie-detail'),
  path('', movie_list, name='movie-list'),
  path('<int:pk>/showtimes', get_showtimes, name='get-showtimes'),
  path('<int:pk>/rating', update_rating, name='rating')
])
