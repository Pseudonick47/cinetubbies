from django.shortcuts import render
from showtimes.serializers import ShowtimeSerializer
from showtimes.models import Showtime
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .permissions import IsThisTheaterAdminOrReadOnly
from django.shortcuts import get_object_or_404
from sale_tickets.models import Booking
from theaters.models import Auditorium

class ShowtimeViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows showtimes to be viewed or edited.
  """
  queryset = Showtime.objects.all()
  serializer_class = ShowtimeSerializer
  permission_classes = [IsThisTheaterAdminOrReadOnly]

  def create(self, request):
    serializer = ShowtimeSerializer(data=request.data, partial=True)
    if not serializer.is_valid():
      return Response(serializer.errors, status=400)
    bookings = []
    seat_num = 1
    showtime = serializer.save()

    auditorium = Auditorium.objects.get(id=request.data['auditorium'])
    layout = auditorium.layout['layout']
    for row in layout:
      for seat in row:
        bookings.append(Booking(showtime_id=showtime.id, seat=seat_num, user_id=None))
        seat_num += 1
    Booking.objects.bulk_create(bookings)

    return Response(serializer.data)

  def destroy(self, request, pk=None):
    showtime = get_object_or_404(Showtime, id=pk)
    self.check_object_permissions(request, showtime)
    showtime.delete()
    return Response({'message': 'Showtime successfully deleted'})

  def retrieve(self, request, pk=None):
    showtime = get_object_or_404(Showtime, id=pk)
    return Response(data=ShowtimeSerializer(showtime).data)

  def update(self, request, pk=None):
    showtime = get_object_or_404(Showtime, id=pk)
    self.check_object_permissions(request, showtime)
    serializer = ShowtimeSerializer(showtime, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)
