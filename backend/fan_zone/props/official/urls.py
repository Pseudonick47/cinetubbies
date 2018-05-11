from django.urls import path

from cinetubbies.utils.routing import BaseManageView

from .views import PublicAPI
from .views import RestrictedAPI


class OfficialProps(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicAPI.as_view({'get': 'list'}),
    'POST': RestrictedAPI.as_view({'post': 'create'})
  }


class OfficialProp(BaseManageView):
  VIEWS_BY_METHOD = {
    'DELETE': RestrictedAPI.as_view({'delete': 'destroy'}),
    'GET': PublicAPI.as_view({'get': 'retrieve'}),
    'PUT': RestrictedAPI.as_view({'put': 'update'})
  }


count_official_props = PublicAPI.as_view({
  'get': 'count'
})


urlpatterns = [
  path(
    route='',
    view=OfficialProps.as_view(),
    name='official-props'
  ),
  path(
    route='count',
    view=count_official_props,
    name='count-official-props'
  ),
  path(
    route='<int:pk>',
    view=OfficialProp.as_view(),
    name="official-prop"
  ),
]
