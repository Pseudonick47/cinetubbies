from django.shortcuts import get_object_or_404

from rest_framework import serializers

from rest_framework.validators import UniqueValidator

from theaters.models import Theater

from .models import ROLES
from .models import TheaterAdmin
from .models import User
from .models import USER
from media_upload.models import Image
from media_upload.serializers import ImageSerializer

class FriendSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  username = serializers.CharField(required=False, allow_blank=False, max_length=30)
  email = serializers.CharField(required=False, allow_blank=True)
  first_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
  last_name = serializers.CharField(required=False, allow_blank=True, max_length=30)
  birth_date = serializers.DateTimeField(required=False)
  phone = serializers.CharField(max_length=30, allow_blank=False)
  city = serializers.CharField(max_length=30, allow_blank=False)

class UserSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  username = serializers.CharField(
    required=False,
    allow_blank=False,
    max_length=30,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  email = serializers.CharField(
    required=False,
    allow_blank=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  first_name = serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=30
  )
  last_name = serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=30
  )
  role = serializers.ChoiceField(
    choices=ROLES,
    default='user'
  )
  password = serializers.CharField(
    write_only=True,
    min_length=5
  )
  birth_date = serializers.DateTimeField(
    required=False
  )
  phone = serializers.CharField(
    max_length=30,
    allow_blank=False
  )
  city = serializers.CharField(
    max_length=30,
    allow_blank=False
  )
  friends_count = serializers.IntegerField(
    read_only=True
  ),
  friend_requests = serializers.ListField(
    read_only=True,
    child = FriendSerializer(),
  )
  friends = serializers.ListField(
    read_only=True,
    child = FriendSerializer(),
  )
  image_id = serializers.PrimaryKeyRelatedField(
    queryset=Image.objects.all(),
    allow_null=True,
    write_only=True,
    source='image',
    required=False
  )
  image = ImageSerializer(
    required=False,
    allow_null=True
  )

  def create(self, validated_data):
    user = User( ** validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user

  def update(self, user, validated_data):
    user.__dict__.update( ** validated_data)
    if 'password' in validated_data:
      user.set_password(validated_data['password'])
    user.save()
    return user

class AdminSerializer(UserSerializer):
  phone = None
  city = None
  single_use_token = serializers.CharField(
    write_only=True,
    required=False
  )


class TheaterAdminSerializer(AdminSerializer):
  theater = serializers.PrimaryKeyRelatedField(
    queryset=Theater.objects.all(),
    allow_null=True
  )

  def create(self, validated_data):
    admin = TheaterAdmin(**validated_data)
    admin.set_password(validated_data['password'])
    admin.save()
    return admin

  def update(self, theater_admin, validated_data):
    theater = get_object_or_404(Theater, pk=validated_data['theater'])
    theater_admin.theater.set(theater)
    return super.update(theater_admin, validated_data)
