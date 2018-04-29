from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from cinetubbies.utils.routing import BaseManageView
from .views import AdministrationAPI
from .views import PublicAPI
from .views import RestrictedAPI


class TheatersManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicAPI.as_view({'get': 'list'}),
    'POST': AdministrationAPI.as_view({'post': 'create'}),
  }

class TheaterManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'DELETE': AdministrationAPI.as_view({'delete': 'destroy'}),
    'GET': PublicAPI.as_view({'get': 'retrieve'}),
    'PUT': RestrictedAPI.as_view({'put': 'update'}),
  }

get_theaters = PublicAPI.as_view({
  'get': 'get_theaters'
})

rating = PublicAPI.as_view({
  'post': 'update_rating'
})

count_theaters = PublicAPI.as_view({
  'get': 'count',
})

update_admins = AdministrationAPI.as_view({
  'put': 'update',
})

get_theater = PublicAPI.as_view({
  'get': 'get_theater'
})

urlpatterns = format_suffix_patterns([
  path('', TheatersManageView.as_view(), name='theaters'),
  path('count', count_theaters, name="count-theaters"),
  path('all', get_theaters, name='get-theaters'),
  path('<int:pk>', TheaterManageView.as_view(), name='theater'),
  path('<int:pk>/admins/', update_admins, name='update-admins'),
  path('rating', rating, name='rating'),
  path('specific/<int:pk>', get_theater, name='get-theater')
])
