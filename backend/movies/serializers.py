from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  title = serializers.CharField(required=True, allow_blank=False, max_length=255)
  genre = serializers.CharField(required=True, allow_blank=False, max_length=255)
  director = serializers.CharField(max_length=255, allow_blank=True)
  actors = serializers.CharField(max_length=255, allow_blank=True)
  duration = serializers.CharField(max_length=255, allow_blank=True)
  description = serializers.CharField(max_length=255, allow_blank=True)

  def create(self, validated_data):
    movie = Movie.objects.create(**validated_data)
    return movie