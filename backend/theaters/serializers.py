from rest_framework import serializers
from .models import Theater, THEATER_KIND


class TheaterSerializer(serializers.Serializer):
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
    admin_id = serializers.IntegerField(
        required=True,
    )
    kind = serializers.ChoiceField(
        required=True,
        allow_blank=False,
        choices=THEATER_KIND
    )

    def create(self, validated_data):
        return Theater.objects.create(**validated_data)

    def update(self, theater, validated_data):
        for k, v in validated_data.items():
            if k != 'admin':
                setattr(theater, k, v)

        theater.save()

        return theater
