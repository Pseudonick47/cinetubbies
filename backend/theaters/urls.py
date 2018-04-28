from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from cinetubbies.util.routing import BaseManageView
from .views import AdministrationAPI
from .views import PublicAPI
from .views import RestrictedAPI


class TheatersManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicAPI.list,
    'POST': AdministrationAPI.create,
  }

class TheaterManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'DELETE': AdministrationAPI.destroy,
    'GET': PublicAPI.retrieve,
    'PUT': RestrictedAPI.update,
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

urlpatterns = format_suffix_patterns([
  path('', TheatersManageView.as_view(), name='theaters'),
  path('count', count_theaters, name="count-theaters"),
  path('all', get_theaters, name='get-theaters'),
  path('<int:pk>', TheaterManageView.as_view(), name='theater'),
  path('<int:pk>/admins', update_admins, name='update-admins'),
  path('rating', rating, name='rating')
])
