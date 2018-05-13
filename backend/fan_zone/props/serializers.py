from rest_framework import serializers

from cinetubbies.utils.func import deepcopy

from media_upload.models import Image
from media_upload.serializers import ImageSerializer


class PropSerializer(serializers.Serializer):
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
  image_id = serializers.PrimaryKeyRelatedField(
    queryset=Image.objects.all(),
    required=False,
    allow_null=True,
    write_only=True,
    source='image'
  )
  image = ImageSerializer(
    read_only=True
  )
  post_date = serializers.DateField(
    read_only=True,
  )
  kind = serializers.CharField(
    source='get_kind',
    read_only=True
  )

  def to_internal_value(self, data):
    if 'imageId' in data:
      d = deepcopy(data)
      d['image_id'] = d.pop('imageId')
      return super().to_internal_value(d)
    return super().to_internal_value(data)

  def to_representation(self, obj):
    ret = super().to_representation(obj)
    ret['postDate'] = ret.pop('post_date')
    return ret
