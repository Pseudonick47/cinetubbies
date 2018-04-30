from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from cinetubbies.utils.routing import BaseManageView

from .views import PublicOfficialPropAPI
from .views import RestrictedOfficialPropAPI
from .views import PublicCategoryAPI
from .views import AdminCategoryAPI


class OfficialPropsManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicOfficialPropAPI.as_view({'get': 'list'}),
    'POST': RestrictedOfficialPropAPI.as_view({'post': 'create'})
  }

class OfficialPropManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'DELETE': RestrictedOfficialPropAPI.as_view({'delete': 'destroy'}),
    'GET': PublicOfficialPropAPI.as_view({'get': 'retrieve'}),
    'PUT': RestrictedOfficialPropAPI.as_view({'put': 'update'})
  }

class CategoriesManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicCategoryAPI.as_view({'get': 'list'}),
    'POST': AdminCategoryAPI.as_view({'post': 'create'})
  }

class CategoryManageView(BaseManageView):
  VIEWS_BY_METHOD = {
    'DELETE': AdminCategoryAPI.as_view({'delete': 'destroy'}),
    'GET': PublicCategoryAPI.as_view({'get': 'retrieve'}),
    'PUT': AdminCategoryAPI.as_view({'put': 'update'})
  }

count_official_props = PublicOfficialPropAPI.as_view({
  'get': 'count'
})

urlpatterns = format_suffix_patterns([
  path(
    route='official-props/',
    view=OfficialPropsManageView.as_view(),
    name='official-props'
  ),
  path(
    route='official-props/count',
    view=count_official_props,
    name='count-official-props'
  ),
  path(
    route='official-props/<int:pk>',
    view=OfficialPropManageView.as_view(),
    name="official-prop"
  ),
  path(
    route='categories/',
    view=CategoriesManageView.as_view(),
    name='categories'
  ),
  path(
    route='categories/<int:pk>',
    view=CategoryManageView.as_view(),
    name='category'
  ),
])