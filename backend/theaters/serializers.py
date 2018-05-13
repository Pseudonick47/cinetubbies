from rest_framework import serializers
import json
from cinetubbies.utils.func import update

from authentication.models import TheaterAdmin
from authentication.models import User

from media_upload.models import Image
from media_upload.serializers import ImageSerializer

from .models import Theater
from .models import Auditorium
from .models import THEATER_KIND

class PublicSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  name = serializers.CharField(
    required=True,
    allow_blank=False,
    max_length=100
  )
  address = serializers.CharField(
    required=True,
    allow_blank=False,
    max_length=300
  )
  description = serializers.CharField(
    required=False,
    allow_blank=True
  )
  kind = serializers.ChoiceField(
    required=True,
    allow_blank=False,
    choices=THEATER_KIND
  )
  voters_count = serializers.IntegerField(source='get_voters_count')
  rating = serializers.DecimalField(
    source='get_avg_rating',
    max_digits=2,
    decimal_places=1
  )
  all_votes = serializers.DictField(
    source='get_all_votings',
    child=serializers.IntegerField()
  )
  image_id = serializers.PrimaryKeyRelatedField(
    queryset=Image.objects.all(),
    allow_null=True,
    write_only=True,
    source='image',
    required=False
  )
  image = ImageSerializer(
    read_only=True
  )

class RestrictedSerializer(PublicSerializer):
  voters_count = None
  rating = None
  all_votes = None

  def update(self, theater, validated_data):
    theater = update(theater, **validated_data)
    theater.save()
    return theater

class AdministrationSerializer(RestrictedSerializer):
  admins = serializers.PrimaryKeyRelatedField(
    queryset=TheaterAdmin.objects.all(),
    many=True
  )

  def create(self, validated_data):
    admins = validated_data.pop('admins')
    theater = Theater.objects.create(**validated_data)
    theater.admins.set(admins)
    return theater

class AuditoriumSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  name = serializers.CharField()
  layout = serializers.JSONField()
  theater = serializers.PrimaryKeyRelatedField(
    queryset=Theater.objects.all(),
    allow_null=False,
    write_only=True,
    required=True
  )

  def create(self, validated_data):
    return Auditorium.objects.create(**validated_data)

  def update(self, auditorium, validated_data):
    auditorium = update(auditorium, **validated_data)
    return auditorium
