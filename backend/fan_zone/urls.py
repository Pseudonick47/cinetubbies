from .props.urls import urlpatterns as prop_urls
from .categories.urls import urlpatterns as category_urls


urlpatterns = prop_urls + category_urls
