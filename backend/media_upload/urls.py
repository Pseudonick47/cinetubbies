from django.urls import path
from django.urls import include

from rest_framework.urlpatterns import format_suffix_patterns

from cinetubbies.utils.routing import BaseManageView

from .views import PublicAPI
from .views import RestrictedAPI


class ImagesManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicAPI.as_view({'get': 'list'}),
    'POST': RestrictedAPI.as_view({'post': 'create'}),
  }

class ImageManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'DELETE': RestrictedAPI.as_view({'delete': 'destroy'}),
    'GET': PublicAPI.as_view({'get': 'retrieve'}),
    'PUT': RestrictedAPI.as_view({'put': 'update'}),
  }

urlpatterns = format_suffix_patterns([
  path('images/', include([
    path('', ImagesManageView.as_view(), name='images'),
    path('<int:pk>', ImageManageView.as_view(), name='image')
  ])),
])
