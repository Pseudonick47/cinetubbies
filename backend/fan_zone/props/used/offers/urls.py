from django.urls import path

from cinetubbies.utils.routing import BaseManageView

from .views import MemberAPI
from .views import PublicAPI


class OffersByUser(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': MemberAPI.as_view({'get': 'list'}),
  }


class OfferByUser(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': MemberAPI.as_view({'get': 'retrieve'}),
    'DELETE': MemberAPI.as_view({'delete': 'destroy'})
  }


class OffersByProp(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicAPI.as_view({'get': 'list'}),
    'POST': MemberAPI.as_view({'post': 'create'})
  }


class OfferByProp(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': PublicAPI.as_view({'get': 'retrieve'}),
  }


count_offers_by_user = MemberAPI.as_view({'get': 'count'})

count_offers_by_prop = PublicAPI.as_view({'get': 'count'})


urls_by_user = [
  path(
    route='',
    view=OffersByUser.as_view(),
    name='offers-by-user'
  ),
  path(
    route='count',
    view=count_offers_by_user,
    name='count-offers-by-user'
  ),
  path(
    route='<int:pk>',
    view=OfferByUser.as_view(),
    name='offer-by-user'
  ),
]

urls_by_props = [
  path(
    route='',
    view=OffersByProp.as_view(),
    name='offers-by-prop'
  ),
  path(
    route='count',
    view=count_offers_by_prop,
    name='count-offers-by-prop'
  ),
  path(
    route='<int:pk>',
    view=OfferByProp.as_view(),
    name='offer-by-prop'
  ),
]

urlpatterns = []