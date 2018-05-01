from rest_framework import serializers

from .models import Image
from .models import IMAGE_KIND


class ImageSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  kind = serializers.ChoiceField(
    write_only=True,
    required=True,
    choices=IMAGE_KIND
  )
  data = serializers.ImageField(
    write_only=True,
    required=True,
    allow_empty_file=False
  )
  path = serializers.ImageField(
    read_only=True,
    source='data'
  )

  def create(self, validated_data):
    return Image.objects.create(**validated_data)

  def update(self, image, validated_data):
    for k, v in validated_data.items():
      setattr(image, k, v)
    image.save()
    return image
