from rest_framework import serializers

from cinetubbies.utils.func import deepcopy
from cinetubbies.utils.func import update

from theaters.models import Theater
from theaters.serializers import PublicSerializer as TheaterSerializer

from fan_zone.categories.models import Category
from fan_zone.categories.serializers import PublicSerializer as \
                                            CategorySerializer
from fan_zone.props.serializers import PropSerializer

from .models import OfficialProp


class PublicSerializer(PropSerializer):
  theater = TheaterSerializer(
    read_only=True,
  )
  category = CategorySerializer(
    read_only=True,
  )
  quantity = serializers.IntegerField(required=True)
  price= serializers.FloatField(required=True)


class RestrictedSerializer(PublicSerializer):
  category_id = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(),
    allow_null=False,
    write_only=True,
    source="category"
  )
  theater_id = serializers.PrimaryKeyRelatedField(
    queryset=Theater.objects.all(),
    allow_null=False,
    write_only=True,
    source="theater"
  )

  def to_internal_value(self, data):
    d = deepcopy(data)
    d['category_id'] = d.pop('categoryId')
    d['theater_id'] = d.pop('theaterId')
    return super().to_internal_value(d)

  def create(self, validated_data):
    return OfficialProp.objects.create(**validated_data)

  def update(self, official_prop, validated_data):
    official_prop = update(official_prop, **validated_data)
    official_prop.save()
    return official_prop
