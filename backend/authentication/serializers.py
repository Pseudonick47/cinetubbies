from rest_framework import serializers
from .models import User, ROLES


class UserSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  username = serializers.CharField(required=True, allow_blank=False, max_length=30)
  password = serializers.CharField(required=True, allow_blank=False, max_length=255)
  first_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
  last_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
  role = serializers.ChoiceField(choices=ROLES, default='user')
  bio = serializers.CharField(max_length=500)
  email = serializers.CharField(required=True, allow_blank=False, max_length=254)

  def create(self, validated_data):
    return User.objects.create(**validated_data)

  def update(self, instance, validated_data):
    instance.save()
    return instance
