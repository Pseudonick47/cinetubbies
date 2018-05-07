from rest_framework import serializers
from .models import Movie, Theater

class MovieSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  title = serializers.CharField(required=True, allow_blank=False, max_length=255)
  genre = serializers.CharField(required=True, allow_blank=False, max_length=255)
  director = serializers.CharField(required=False, max_length=255, allow_blank=True)
  actors = serializers.CharField(required=False, max_length=255, allow_blank=True)
  duration = serializers.CharField(required=False, max_length=255, allow_blank=True)
  description = serializers.CharField(required=False, max_length=255, allow_blank=True)
  theater = serializers.PrimaryKeyRelatedField(queryset=Theater.objects.all(),allow_null=False)
  voters_count = serializers.IntegerField(required=False, source='get_voters_count')
  rating = serializers.DecimalField(required=False, source='get_avg_rating', max_digits=2, decimal_places=1)
  all_votes = serializers.DictField(required=False, source='get_all_votings', child=serializers.IntegerField())

  def create(self, validated_data):
    movie = Movie.objects.create(**validated_data)
    movie.save()
    return movie

  def update(self, movie, validated_data):
    for k, v in validated_data.items():
      setattr(movie, k, v)
    movie.save()
    return movie