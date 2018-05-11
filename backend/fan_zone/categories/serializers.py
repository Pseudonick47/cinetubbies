from rest_framework import serializers

from cinetubbies.utils.func import update

from .models import Category


class PublicSerializer(serializers.Serializer):
  # TODO: change to AutoField
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


class AdministrationSerializer(PublicSerializer):

  def create(self, validated_data):
    return Category.objects.create(**validated_data)

  def update(self, category, validated_data):
    category = update(category, **validated_data)
    category.save()
    return category
