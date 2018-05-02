from rest_framework import serializers

from cinetubbies.utils.func import update

from .models import REWARD_STATUS


class RewardScaleSerializer(serializers.Serializer):
  status = serializers.ChoiceField(choices=REWARD_STATUS)
  min_points = serializers.IntegerField(
    required=True,
    allow_null=False,
    min_value=0,
    max_value=32767
  )
  max_points = serializers.IntegerField(
    required=True,
    allow_null=False,
    min_value=0,
    max_value=32767
  )

  def validate(self, data):
    if data['min_points'] > data['max_points']:
      raise serializers.ValidationError(
        'max_points has to be greater than or equal to min_points'
      )
    return data

  def update(self, scale, validated_data):
    update(scale, **validated_data)
    scale.save()
    return scale
