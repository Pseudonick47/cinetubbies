from django.shortcuts import render
from showtimes.serializers import ShowtimeSerializer
from showtimes.models import Showtime
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
# from .permissions import IsCreatorOrReadOnly
# from authentication.models import TheaterAdmin
from django.shortcuts import get_object_or_404

class ShowtimeViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows showtimes to be viewed or edited.
  """
  queryset = Showtime.objects.all()
  serializer_class = ShowtimeSerializer
  # permission_classes = [IsCreatorOrReadOnly]

  def create(self, request):
    serializer = ShowtimeSerializer(data=request.data, partial=True)
    if not serializer.is_valid():
      return Response(serializer.errors, status=400)
    serializer.save()
    return Response(serializer.data)

  def list(self, request):
    showtimes = Showtime.objects.all()
    return Response(ShowtimeSerializer(showtimes, many=True).data)

  def destroy(self, request, pk=None):
    showtime = Showtime.objects.get(id=pk)
    # self.check_object_permissions(request, showtime)
    showtime.delete()
    return Response({'message': 'Showtime successfully deleted'})

  def retrieve(self, request, pk=None):
    showtime = Showtime.objects.get(id=pk)
    return Response(data=ShowtimeSerializer(showtime).data)

  def update(self, request, pk=None):
    showtime = get_object_or_404(Showtime, id=pk)
    serializer = ShowtimeSerializer(showtime, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)
