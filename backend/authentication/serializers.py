from rest_framework import serializers
from .models import User, ROLES


class UserSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  username = serializers.CharField(required=False, allow_blank=False, max_length=30)
  email = serializers.CharField(required=False, allow_blank=True)
  first_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
  last_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
  role = serializers.ChoiceField(choices=ROLES, default='user')
  password = serializers.CharField(write_only=True, min_length=5)
  birth_date = serializers.DateTimeField(required=False)

  def create(self, validated_data):
    user = User(
        username=validated_data['username'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

  def update(self, user, validated_data):
    user.__dict__.update( ** validated_data)
    if 'password' in validated_data:
      user.set_password(validated_data['password'])
    user.save()
    return user
