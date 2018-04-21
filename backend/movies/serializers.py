from rest_framework import serializers
#from .models import User, ROLES

class MovieSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  title = serializers.CharField(required=True, allow_blank=False, max_length=30)
  genre = serializers.CharField(required=True, allow_blank=False, max_length=30)

  def create(self, validated_data):
    return Movie.objects.create(**validated_data)