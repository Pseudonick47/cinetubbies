from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.permissions import IsFanZoneOrSystemAdmin

from cinetubbies.utils.models import ObjectLocked

from fan_zone.props.models import Prop
from fan_zone.props.models import USED_PROP

from .models import Offer
from .permissions import IsOwner
from .serializers import MemberSerializer
from .serializers import PublicSerializer


class PublicAPI(ViewSet):
  permission_classes = [AllowAny]

  @action(detail=False)
  def count(self, request, *args, **kwargs):
    prop_id = kwargs.pop('prop_id')
    queryset = Offer.objects.filter(prop_id=prop_id)
    return Response(data=queryset.count())

  def list(self, request, *args, **kwargs):
    prop_id = kwargs.pop('prop_id')
    offers = Offer.objects.filter(prop_id=prop_id).all()
    return Response(data=PublicSerializer(offers, many=True).data)

  def retrieve(self, request, *args, **kwargs):
    offer = get_object_or_404(Offer, pk=kwargs.pop('pk'))
    return Response(data=PublicSerializer(offer).data)


class MemberAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsOwner]

  def create(self, request, *args, **kwargs):
    prop_id = kwargs.pop('prop_id')
    prop = get_object_or_404(Prop, pk=prop_id)

    if prop.kind != USED_PROP[0]:
      return Response(
        data="Placing offers on official props is not supported.",
        status=status.HTTP_400_BAD_REQUEST
      )

    if prop.owner.id == request.user.id:
      return Response(
        data="User is not allowed to place an offer on his own prop ad.",
        status=status.HTTP_400_BAD_REQUEST
      )

    amount = request.data.get('amount', None)
    if not sum:
      return Response(
        data="Amount is required.",
        status=status.HTTP_400_BAD_REQUEST
      )

    offer = Offer.objects.create(
      user_id=request.user.id,
      prop_id=prop_id,
      amount=amount
    )

    return Response(data=PublicSerializer(offer).data)

  @action(detail=False)
  def count(self, request, *args, **kwargs):
    user_id = kwargs.pop('user_id')
    queryset = Offer.objects.filter(user_id=user_id)
    return Response(data=queryset.count())

  def destroy(self, request, *args, **kwargs):
    offer = get_object_or_404(Offer, pk=kwargs.pop('pk'))
    self.check_object_permissions(request, offer)
    offer.delete()
    return Response(
      data=PublicSerializer(offer).data
    )

  def list(self, request, *args, **kwargs):
    user_id = kwargs.pop('user_id')
    offers = Offer.objects.filter(user_id=user_id).all()
    return Response(data=PublicSerializer(offers, many=True).data)

  def retrieve(self, request, *args, **kwargs):
    offer = get_object_or_404(Offer, pk=kwargs.pop('pk'))
    self.check_object_permissions(request, offer)
    return Response(data=PublicSerializer(offer).data)
