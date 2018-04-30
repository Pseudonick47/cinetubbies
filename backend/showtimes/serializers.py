from rest_framework import serializers
from .models import Movie, Showtime

class ShowtimeSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  auditorium = serializers.CharField(max_length=255, allow_blank=False, required=True)
  date = serializers.DateField(required=True)
  time = serializers.TimeField(required=True)
  price = serializers.DecimalField(max_digits=6, decimal_places=2, required=True)
  movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), allow_null=False)

  def create(self, validated_data):
    showtime = Showtime.objects.create(**validated_data)
    showtime.save()
    return showtime

  def update(self, showtime, validated_data):
    for k, v in validated_data.items():
      setattr(showtime, k, v)
    showtime.save()
    return showtime