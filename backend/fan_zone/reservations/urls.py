from django.urls import path

from cinetubbies.utils.routing import BaseManageView

from fan_zone.reservations.views import MemberAPI
from fan_zone.reservations.views import RestrictedAPI


class ReservationsByUser(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': MemberAPI.as_view({'get': 'list'}),
  }


class ReservationByUser(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': MemberAPI.as_view({'get': 'retrieve'}),
    'DELETE': MemberAPI.as_view({'delete': 'destroy'})
  }


class ReservationsByProp(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': RestrictedAPI.as_view({'get': 'list'}),
    'POST': MemberAPI.as_view({'post': 'create'})
  }


class ReservationByProp(BaseManageView):
  VIEWS_BY_METHOD = {
    'GET': RestrictedAPI.as_view({'get': 'retrieve'}),
  }


count_reservations_by_user = MemberAPI.as_view({'get': 'count'})

count_reservations_by_prop = RestrictedAPI.as_view({'get': 'count'})


urls_by_user = [
  path(
    route='',
    view=ReservationsByUser.as_view(),
    name='reservations-by-user'
  ),
  path(
    route='count',
    view=count_reservations_by_user,
    name='count-reservations-by-user'
  ),
  path(
    route='<int:pk>',
    view=ReservationByUser.as_view(),
    name='reservation-by-user'
  ),
]

urls_by_props = [
  path(
    route='',
    view=ReservationsByProp.as_view(),
    name='reservations-by-prop'
  ),
  path(
    route='count',
    view=count_reservations_by_prop,
    name='count-reservations-by-prop'
  ),
  path(
    route='<int:pk>',
    view=ReservationByProp.as_view(),
    name='reservation-by-prop'
  ),
]

urlpatterns = []