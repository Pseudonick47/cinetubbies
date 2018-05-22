from django.urls import include
from django.urls import path

from .views import PublicAPI

from .official.urls import urlpatterns as official_urls
from .used.urls import urlpatterns as used_urls


props = PublicAPI.as_view({'get': 'list'})

prop = PublicAPI.as_view({'get': 'retrieve'})

count_props = PublicAPI.as_view({'get': 'count'})


prop_urls = [
  path('official/', include(official_urls)),
  path('used/', include(used_urls)),
]


urlpatterns = [
  path(
    route='',
    view=props,
    name='props'
  ),
  path(
    route='count',
    view=count_props,
    name='count-props'
  ),
  path(
    route='<int:pk>',
    view=prop,
    name='prop'
  ),
] + prop_urls
