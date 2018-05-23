from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.permissions import IsFanZoneOrSystemAdmin

from cinetubbies.utils.models import ObjectLocked

from fan_zone.props.models import Prop
from fan_zone.props.models import OFFICIAL_PROP

from .models import Reservation
from .permissions import IsOwner
from .serializers import MemberSerializer
from .serializers import PublicSerializer


class MemberAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsOwner]

  def create(self, request, *args, **kwargs):
    prop_id = kwargs.pop('prop_id')
    prop = get_object_or_404(Prop, pk=prop_id)

    if prop.kind != OFFICIAL_PROP[0]:
      return Response(
        data="Used prop reservations are not supported.",
        status=status.HTTP_400_BAD_REQUEST
      )

    quantity = request.data.get('quantity', None)
    if not quantity:
      return Response(
        data="Quantity is required.",
        status=status.HTTP_400_BAD_REQUEST
      )

    prop.quantity -= quantity
    try:
      prop.save()
    except ValueError:
      return Response(
        data="No available props.",
        status=status.HTTP_409_CONFLICT
      )
    except ObjectLocked:
      return Response(
        status=status.HTTP_423_LOCKED
      )

    reservation = Reservation.objects.create(
      user_id=request.user.id,
      prop_id=prop_id,
      quantity=quantity
    )

    return Response(data=PublicSerializer(reservation).data)

  @action(detail=False)
  def count(self, request, *args, **kwargs):
    user_id = kwargs.pop('user_id')
    queryset = Reservation.objects.filter(user_id=user_id)
    return Response(data=queryset.count())

  def destroy(self, request, *args, **kwargs):
    reservation = get_object_or_404(Reservation, pk=kwargs.pop('pk'))
    self.check_object_permissions(request, reservation)
    reservation.prop.quantity += reservation.quantity

    try:
      reservation.prop.save()
    except ObjectLocked:
      # TODO: rework
      pass

    reservation.delete()
    return Response(
      data=PublicSerializer(reservation).data
    )

  def list(self, request, *args, **kwargs):
    user_id = kwargs.pop('user_id')
    reservations = Reservation.objects.filter(user_id=user_id).all()
    return Response(data=PublicSerializer(reservations, many=True).data)

  def retrieve(self, request, *args, **kwargs):
    reservation = get_object_or_404(Reservation, pk=kwargs.pop('pk'))
    self.check_object_permissions(request, reservation)
    return Response(data=PublicSerializer(reservation).data)


class RestrictedAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsFanZoneOrSystemAdmin]

  @action(detail=False)
  def count(self, request, *args, **kwargs):
    prop_id = kwargs.pop('prop_id')
    queryset = Reservation.objects.filter(prop_id=prop_id)
    return Response(data=queryset.count())

  def list(self, request, *args, **kwargs):
    prop_id = kwargs.pop('prop_id')
    reservations = Reservation.objects.filter(prop_id=prop_id).all()
    return Response(data=PublicSerializer(reservations, many=True).data)

  def retrieve(self, request, *args, **kwargs):
    reservation = get_object_or_404(Reservation, pk=kwargs.pop('pk'))
    if reservation.prop_id != kwargs.pop('prop_id'):
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(data=PublicSerializer(reservation).data)
