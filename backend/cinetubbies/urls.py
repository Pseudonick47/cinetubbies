from django.contrib import admin
from django.urls import path, include
# from rest_framework_jwt.views import obtain_jwt_token
from authentication import urls

urlpatterns = [
  path('api/', include([
    path('', include('authentication.urls')),
    path('content/', include('theaters.urls')),
  ])),
  path('admin/', admin.site.urls),
]
