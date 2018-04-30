from django.urls import include
from django.urls import path

from cinetubbies.utils.routing import BaseManageView

from fan_zone.urls import prop_urls

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

urlpatterns = [
  path(
    route='',
    view=TheatersManageView.as_view(),
    name='theaters'
  ),
  path(
    route='count',
    view=count_theaters,
    name="count-theaters"
  ),
  path(
    route='all',
    view=get_theaters,
    name='get-theaters'
  ),
  path(
    route='<int:pk>',
    view=TheaterManageView.as_view(),
    name='theater'
  ),
  path(
    route='<int:pk>/admins/',
    view=update_admins,
    name='update-admins'
  ),
  path(
    route='<int:theater_pk>/props/',
    view=include(prop_urls),
  ),
  path(
    route='rating',
    view=rating,
    name='rating'
  ),
]
