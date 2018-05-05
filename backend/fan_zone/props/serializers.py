import copy

from rest_framework import serializers

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
    allow_null=True,
    write_only=True,
    source='image'
  )
  image = ImageSerializer(
    read_only=True
  )

  def to_internal_value(self, data):
    d = copy.deepcopy(data)
    d['image_id'] = d.pop('imageId')
    return super().to_internal_value(d)
