from django.shortcuts import render
from .serializers import BookingSerializer
from .serializers import TicketOnSaleSerializer
from .models import TicketOnSale
from .models import Booking
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from .permissions import IsThisTheaterAdminOrReadOnly, IsSelfOrReadOnly
from django.shortcuts import get_object_or_404

class TicketOnSaleViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows tickets on sale to be viewed or edited.
  """
  queryset = TicketOnSale.objects.all()
  serializer_class = TicketOnSaleSerializer
  permission_classes = [IsThisTheaterAdminOrReadOnly]

  def create(self, request):
    serializer = TicketOnSaleSerializer(data=request.data, partial=True)
    if not serializer.is_valid():
      return Response(serializer.errors, status=400)
    serializer.save()
    return Response(serializer.data)

  def destroy(self, request, pk=None):
    ticket = get_object_or_404(TicketOnSale, pk=pk)
    self.check_object_permissions(request, ticket)
    ticket.delete()
    return Response({'message': 'Ticket successfully deleted'})

  def retrieve(self, request, pk=None):
    ticket = get_object_or_404(TicketOnSale, pk=pk)
    return Response(data=TicketOnSaleSerializer(ticket).data)

  def update(self, request, pk=None):
    ticket = get_object_or_404(TicketOnSale, id=pk)
    self.check_object_permissions(request, ticket)
    serializer = TicketOnSaleSerializer(ticket, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

class BookingViewSet(viewsets.ViewSet):
  """
  API endpoint for CRUD actions on bookings.
  """
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

  def list(self, request):
    bookings = Booking.objects.all()
    return Response(data=BookingSerializer(bookings, many=True).data)

  def create(self, request):
    request.data['user'] = request.user.id
    # provera da li je zauzeto i zakljucavanje svih od jednom
    seat_ids = request.data['choosenSeats']

    updated_bookings = []
    for seat in seat_ids:
      request.data['seat'] = seat
      place = Booking.objects.filter(showtime_id=request.data['showtime'], seat=request.data['seat'])[0]
      if not place.user is None:
        return Response({'message': 'Booking failed. Are all the seats empty?'}, status=400)
      place.user_id = request.user.id

      if 'discount' in request.data:
        place.discount = request.data['discount']
        ticket = TicketOnSale.objects.filter(showtime_id=request.data['showtime'],seat=request.data['seat'])[0]
        serializer = TicketOnSaleSerializer(ticket, data={ 'deleted': 1 }, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

      updated_bookings.append(place)
    # Booking.objects.bulk_update(updated_bookings)
    for s in updated_bookings:
      s.save()
    # otkljucati
    return Response({'message': 'Tickets booked successfully'})

  def destroy(self, request, pk=None):
    booking = get_object_or_404(Booking, id=pk)
    self.check_object_permissions(request, booking)
    booking.delete()
    return Response({'message': 'Booking successfully deleted'})
