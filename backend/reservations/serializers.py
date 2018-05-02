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

  def to_representation(self, obj):
    res = super().to_representation(obj)
    res['min'] = res.pop('min_points')
    res['max'] = res.pop('max_points')
    return res

  def to_internal_value(self, data):
    data['min_points'] = data.pop('min')
    data['max_points'] = data.pop('max')
    return super().to_internal_value(data)

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
