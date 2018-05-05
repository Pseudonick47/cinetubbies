from django.urls import include
from django.urls import path

from cinetubbies.utils.routing import BaseManageView

from .views import PublicAPI
from .views import AdministrationAPI


class Categories(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicAPI.as_view({'get': 'list'}),
    'POST': AdministrationAPI.as_view({'post': 'create'})
  }


class Category(BaseManageView):
  VIEWS_BY_METHOD = {
    'DELETE': AdministrationAPI.as_view({'delete': 'destroy'}),
    'GET': PublicAPI.as_view({'get': 'retrieve'}),
    'PUT': AdministrationAPI.as_view({'put': 'update'})
  }


urlpatterns = [
  path(
    route='categories/',
    view=Categories.as_view(),
    name='categories'
  ),
  path(
    route='categories/<int:pk>',
    view=Category.as_view(),
    name='category'
  ),
]
