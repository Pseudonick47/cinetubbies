from django.urls import include
from django.urls import path

from .official.urls import urlpatterns as official_urls
from .used.urls import urlpatterns as used_urls


prop_urls = [
  path('official/', include(official_urls)),
  path('used/', include(used_urls)),
]


urlpatterns = [
  path(
    route='categories/<int:category_pk>/',
    view=include(prop_urls),
    name='category-props'
  ),
] + prop_urls
