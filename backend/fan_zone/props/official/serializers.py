from rest_framework import serializers

from cinetubbies.utils.func import update

from theaters.models import Theater

from fan_zone.categories.models import Category
from fan_zone.props.serializers import PropSerializer

from .models import OfficialProp


class PublicSerializer(PropSerializer):
  theater = serializers.PrimaryKeyRelatedField(
    queryset=Theater.objects.all(),
    allow_null=False
  )
  category = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(),
    allow_null=False
  )
  quantity = serializers.IntegerField(required=True)
  price= serializers.FloatField(required=True)


class RestrictedSerializer(PublicSerializer):

  def create(self, validated_data):
    return OfficialProp.objects.create(**validated_data)

  def update(self, official_prop, validated_data):
    official_prop = update(official_prop, **validated_data)
    official_prop.save()
    return official_prop
