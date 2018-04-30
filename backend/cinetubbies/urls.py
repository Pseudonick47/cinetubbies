from django.contrib import admin
from django.urls import path, include
from authentication import urls
from movies import urls

urlpatterns = [
  path('api/', include([
    path('', include('authentication.urls')),
    path('theaters/', include('theaters.urls')),
    path('movies/', include('movies.urls'))
  ])),
  path('admin/', admin.site.urls),
]
