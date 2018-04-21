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
    'get': 'list'
})

movie_register = MovieViewSet.as_view({
    'post': 'register',
})

urlpatterns = format_suffix_patterns([
    path('movies/<int:pk>/', movie_detail, name='movie-detail'),
    path('movies/', movie_list, name='movie-list'),
    path('movies/new/', movie_register, name='movie-register'),
])
