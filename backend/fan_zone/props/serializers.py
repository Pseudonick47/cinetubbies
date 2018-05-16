from rest_framework import serializers

from cinetubbies.utils.func import deepcopy

from fan_zone.categories.models import Category
from fan_zone.categories.serializers import PublicSerializer as \
                                            CategorySerializer

from fan_zone.props.models import PROP_KIND

from media_upload.models import Image
from media_upload.serializers import ImageSerializer


class PropSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  title = serializers.CharField(
    max_length=100
  )
  description = serializers.CharField(
    required=False,
    allow_blank=True,
    default=""
  )
  image_id = serializers.PrimaryKeyRelatedField(
    queryset=Image.objects.all(),
    write_only=True,
    required=False,
    allow_null=True,
    source='image'
  )
  image = ImageSerializer(
    read_only=True,
  )
  category_id = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(),
    write_only=True,
    source='category'
  )
  category = CategorySerializer(
    read_only=True,
  )
  post_date = serializers.DateField(
    read_only=True,
  )
  kind = serializers.ChoiceField(
    choices=PROP_KIND
  )

  def to_internal_value(self, data):
    d = deepcopy(data)
    if 'imageId' in d:
      d['image_id'] = d.pop('imageId')
    if 'categoryId' in d:
      d['category_id'] = d.pop('categoryId')
    return super().to_internal_value(d)

  def to_representation(self, obj):
    ret = super().to_representation(obj)
    ret['postDate'] = ret.pop('post_date')
    return ret
