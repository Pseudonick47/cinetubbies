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
    voters_count = serializers.IntegerField(source='get_voters_count')
    rating = serializers.DecimalField(source='get_avg_rating', max_digits=2, decimal_places=1)
    all_votes = serializers.DictField(source='get_all_votings', child=serializers.IntegerField())

    def create(self, validated_data):
        return Theater.objects.create(**validated_data)

    def update(self, theater, validated_data):
        for k, v in validated_data.items():
            if k != 'admin':
                setattr(theater, k, v)

        theater.save()

        return Theater

    class Meta:
        model = Theater
        fields = ('id','name','address','admin_id','kind','voters_count','rating','all_votes')