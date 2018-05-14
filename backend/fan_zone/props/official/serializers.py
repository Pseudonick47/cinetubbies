from rest_framework import serializers

from cinetubbies.utils.func import deepcopy
from cinetubbies.utils.func import update

from fan_zone.props.models import Prop
from fan_zone.props.serializers import PropSerializer

from theaters.models import Theater
from theaters.serializers import PublicSerializer as TheaterSerializer

# from .models import OfficialProp


class PublicSerializer(PropSerializer):
  theater = TheaterSerializer(
    read_only=True,
  )
  quantity = serializers.IntegerField()
  price= serializers.FloatField()


class RestrictedSerializer(PublicSerializer):
  theater_id = serializers.PrimaryKeyRelatedField(
    queryset=Theater.objects.all(),
    write_only=True,
    source="theater"
  )

  def to_internal_value(self, data):
    d = deepcopy(data)
    d['theater_id'] = d.pop('theaterId')
    return super().to_internal_value(d)

  def create(self, validated_data):
    return Prop.objects.create(**validated_data)

  def update(self, official_prop, validated_data):
    official_prop = update(official_prop, **validated_data)
    official_prop.save()
    return official_prop
