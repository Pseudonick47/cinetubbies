from rest_framework import serializers

from cinetubbies.utils.func import update

from authentication.models import FanZoneAdmin
from authentication.models import TheaterAdmin

from .models import Theater
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

class RestrictedSerializer(PublicSerializer):
  voters_count = None
  rating = None
  all_votes = None

  def update(self, theater, validated_data):
    theater = update(theater, **validated_data)
    theater.save()
    return theater

class AdministrationSerializer(RestrictedSerializer):
  theateradmins = serializers.PrimaryKeyRelatedField(
    queryset=TheaterAdmin.objects.all(),
    many=True
  )
  fanzoneadmins = serializers.PrimaryKeyRelatedField(
    queryset=FanZoneAdmin.objects.all(),
    many=True
  )

  def create(self, validated_data):
    theateradmins = validated_data.pop('theateradmins')
    fanzoneadmins = validated_data.pop('fanzoneadmins')
    theater = Theater.objects.create(**validated_data)
    theater.theateradmins.set(theateradmins)
    theater.fanzoneadmins.set(fanzoneadmins)
    return theater
