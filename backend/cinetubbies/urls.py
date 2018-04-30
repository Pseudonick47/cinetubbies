from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from authentication import urls
from movies import urls

urlpatterns = [
  path('api/', include([
    path('', include('authentication.urls')),
    path('theaters/', include('theaters.urls')),
    path('movies/', include('movies.urls')),
    path('media/', include('media_upload.urls')),
    path('fan-zone/', include('fan_zone.urls')),
  ])),
  path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
