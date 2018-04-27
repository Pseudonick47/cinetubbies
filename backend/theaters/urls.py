from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import AdministrationAPI
from .views import PublicAPI
from .views import RestrictedAPI


theater = PublicAPI.as_view({
  'get': 'retrieve',
})

theaters = PublicAPI.as_view({
  'get': 'list',
})

get_theaters = PublicAPI.as_view({
  'get': 'get_theaters'
})

rating = PublicAPI.as_view({
  'post': 'update_rating'
})

count_theaters = PublicAPI.as_view({
  'get': 'count',
})

update_theater = RestrictedAPI.as_view({
  'put': 'update'
})

create_theater = AdministrationAPI.as_view({
  'post': 'create'
})

update_admins = AdministrationAPI.as_view({
  'put': 'update',
})

destroy_theater = AdministrationAPI.as_view({
  'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
  path('', theaters, name='theaters'),
  path('count', count_theaters, name="count-theaters"),
  path('create', create_theater, name="create-theater"),
  path('<int:pk>', theater, name='theater'),
  path('<int:pk>/admins', update_admins, name='update-admins'),
  path('<int:pk>/delete', destroy_theater, name='destroy-theater'),
  path('<int:pk>/update', update_theater, name='update-theater'),
  path('just-theaters/', get_theaters, name='get-theaters'),
  path('rating/', rating, name='rating')
])
