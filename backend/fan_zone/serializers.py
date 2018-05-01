from rest_framework import serializers

from cinetubbies.utils.func import update

from media_upload.models import Image
from media_upload.serializers import ImageSerializer
from theaters.models import Theater

from .models import Category
from .models import OfficialProp


class PublicPropSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  title = serializers.CharField(
    required=True,
    allow_blank=False,
    max_length=100
  )
  description = serializers.CharField(
    required=False,
    allow_blank=True
  )
  category = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(),
    allow_null=False
  )
  image_id = serializers.PrimaryKeyRelatedField(
    queryset=Image.objects.all(),
    allow_null=True,
    write_only=True,
    source='image'
  )
  image = ImageSerializer(
    read_only=True
  )

class PublicOfficialPropSerializer(PublicPropSerializer):
  theater = serializers.PrimaryKeyRelatedField(
    queryset=Theater.objects.all(),
    allow_null=False
  )
  quantity = serializers.IntegerField(required=True)
  price= serializers.FloatField(required=True)


class RestrictedOfficialPropSerializer(PublicOfficialPropSerializer):

  def create(self, validated_data):
    return OfficialProp.objects.create(**validated_data)

  def update(self, official_prop, validated_data):
    official_prop = update(official_prop, **validated_data)
    official_prop.save()
    return official_prop


class PublicCategorySerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  name = serializers.CharField(
    required = True,
    allow_blank=False,
    max_length=30
  )
  supercategory = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(),
    allow_null=True
  )

class AdminCategorySerializer(PublicCategorySerializer):

  def create(self, validated_data):
    return Category.objects.create(**validated_data)

  def update(self, category, validated_data):
    category = update(category, **validated_data)
    category.save()
    return category
