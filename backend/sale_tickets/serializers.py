from rest_framework import serializers

from .models import TicketOnSale
from .models import Booking
from showtimes.models import Showtime
from theaters.models import Theater
from authentication.models import User

class TicketOnSaleSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  theater = serializers.PrimaryKeyRelatedField(queryset=Theater.objects.all(),allow_null=False)
  showtime = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all(),allow_null=False)
  seat = serializers.IntegerField(required=True)
  discount = serializers.IntegerField(required=True)
  deleted = serializers.IntegerField(required=True)

  def create(self, validated_data):
    ticket = TicketOnSale.objects.create(**validated_data)
    ticket.save()
    return ticket

  def update(self, ticket, validated_data):
    for k, v in validated_data.items():
      setattr(ticket, k, v)
    ticket.save()
    return ticket


class BookingSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  showtime = serializers.PrimaryKeyRelatedField(queryset=Showtime.objects.all(), allow_null=False)
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=False)
  discount = serializers.IntegerField(required=False)
  price = serializers.IntegerField(required=False)
  seat = serializers.IntegerField()

  def create(self, validated_data):
    booking = Booking.objects.create(**validated_data)
    booking.save()
    return booking

  def update(self, ticket, validated_data):
    [setattr(booking, k, v) for k, v in validated_data.items()]
    booking.save()
    return ticket