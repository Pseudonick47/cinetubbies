from rest_framework import serializers

from authentication.models import User
from authentication.serializers import UserSerializer

from cinetubbies.utils.func import deepcopy

from fan_zone.props.models import Prop
from fan_zone.props.used.serializers import PublicSerializer as \
                                                PropSerializer

from .models import Offer


class PublicSerializer(serializers.Serializer):
  id = serializers.IntegerField(
    read_only=True
  )
  user =  UserSerializer(
    read_only=True
  )
  prop = PropSerializer(
    read_only=True
  )
  sum = serializers.IntegerField(
    min_value=0
  )

class MemberSerializer(serializers.Serializer):
  user_id =  serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),
    write_only=True,
    source='user'
  )
  prop_id = serializers.PrimaryKeyRelatedField(
    queryset=Prop.official.all(),
    write_only=True,
    source='prop'
  )

  def to_internal_value(self, data):
    d = deepcopy(data)
    d['user_id'] = d.pop('userId')
    d['prop_id'] = d.pop('propId')
    return super().to_internal_value(d)

  def create(self, validate_data):
    return Reservation.objects.create(**validate_data)
