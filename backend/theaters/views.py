from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import TheaterAdmin
from authentication.permissions import IsSystemAdmin
from authentication.permissions import IsTheaterOrSystemAdmin

from media_upload.defaults import DEFAULT_THEATER_IMAGE
from media_upload.models import Image
from media_upload.models import THEATER_IMAGE

from .models import Theater
from .models import Auditorium
from .models import THEATER_KIND
from .models import Voting
from sale_tickets.models import Booking
from .serializers import PublicSerializer
from .serializers import RestrictedSerializer
from .serializers import AdministrationSerializer
from .serializers import AuditoriumSerializer
from .permissions import IsResponsibleForTheater
from movies.serializers import MovieSerializer
from showtimes.serializers import ShowtimeSerializer
from sale_tickets.serializers import TicketOnSaleSerializer


class PublicAPI(ViewSet):
  queryset = Theater.objects.all()
  permission_classes = [AllowAny]

  def list(self, request):
    all = request.GET.get('all')
    # if all:
    #   return Response(data=PublicSerializer(self.queryset, many=True).data)

    num = request.GET.get('num')
    paginator = Paginator(Theater.objects.all().order_by('name'), num if num else 10)
    page = request.GET.get('page')
    theaters = paginator.get_page(page if page else 1)
    return Response(data=PublicSerializer(theaters, many=True).data)

  def retrieve(self, request, pk=None):
    theater = get_object_or_404(Theater, pk=pk)
    return Response(data=PublicSerializer(theater).data)

  @action(detail=False)
  def count(self, request):
    return Response(data=Theater.objects.count())

  @action(detail=False)
  def get_theaters(self, request):
    return Response(data=PublicSerializer(Theater.objects.all(), many=True).data)

  @action(detail=False)
  def get_theater(self, request, pk=None):
    theater_admin = TheaterAdmin.objects.get(user_ptr_id=pk)
    theater = Theater.objects.get(id=theater_admin.theater_id)
    data = PublicSerializer(theater).data
    data['auditoriums'] = AuditoriumSerializer(theater.auditoriums.all(), many=True).data
    return Response(data=data)

  @action(detail=True)
  def update_rating(self, request, pk=None):
    vote, _ = Voting.objects.get_or_create(
      user_id=request.user.id,
      theater_id=pk
    )
    vote.rating = request.data['rating']
    vote.save()
    rating = Voting.objects.filter(
      theater_id=pk).aggregate(rating=Avg('rating')
    )
    voters = len(Voting.objects.filter(theater_id=pk).all())
    data = {'rating':rating,'voters':voters}
    return Response(data)

  @action(detail=True)
  def get_movies(self, request, pk=None):
    theater = Theater.objects.get(id=pk)
    movies = theater.movies.all()
    return Response(MovieSerializer(movies, many=True).data)

  @action(detail=True)
  def get_repertoire(self, request, pk=None):
    theater = Theater.objects.get(id=pk)
    movies = theater.movies.all()
    showtimes = []
    for movie in movies:
      showtime_list = list(movie.showtimes.all())
      for s in showtime_list:
        showtimes.append(s)
    return Response(ShowtimeSerializer(showtimes, many=True).data)

  @action(detail=True)
  def get_tickets_on_sale(self, request, pk=None):
    theater = get_object_or_404(Theater, id=pk)
    tickets = theater.tickets_on_sale.filter(deleted=0)
    return Response(TicketOnSaleSerializer(tickets, many=True).data)

class RestrictedAPI(ViewSet):
  permission_classes = [
    IsAuthenticated,
    IsTheaterOrSystemAdmin,
    IsResponsibleForTheater
  ]

  def update(self, request, pk=None):
    theater = get_object_or_404(Theater, pk=pk)
    self.check_object_permissions(request, theater)
    serializer = RestrictedSerializer(
      theater, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  @action(detail=True)
  def get_revenue(self, request, pk=None):
    all_bookings = Booking.objects.all()
    this_theater_bookings = all_bookings.filter(showtime__movie__theater__id=pk)
    result = 0

    if request.data['type'] == 'all':
      for b in this_theater_bookings:
        result += b.price() - b.get_discount()
    elif request.data['type'] == 'year':
      for b in this_theater_bookings:
        if str(b.date().year) == request.data['year']:
          result += b.price() - b.get_discount()
    elif request.data['type'] == 'month':
      for b in this_theater_bookings:
        if b.date().month < 10:
          month = '0'+str(b.date().month)
        else:
          month = str(b.date().month)

        if str(b.date().year) == str(request.data['month'].split('-')[0]) and month == str(request.data['month'].split('-')[1]):
          result += b.price() - b.get_discount()
    else:
      for b in this_theater_bookings:
        if str(b.date()) >= request.data['date1'] and str(b.date()) <= request.data['date2']:
          result += b.price() - b.get_discount()

    return Response(result)

  @action(detail=True)
  def get_attendance(self, request, pk=None, period=None):
    all_bookings = Booking.objects.all()
    this_theater_bookings = list(all_bookings.filter(showtime__movie__theater__id=pk).exclude(user_id__isnull=True))
    result = []
    date = datetime.now()

    if period == 'overall':
      result.append(len(this_theater_bookings))
    elif period == 'year':
      this_year_bookings = [b for b in this_theater_bookings if b.showtime.date.year == date.year]
      for i in range(1, 13):
        result.append(len( [b for b in this_year_bookings if b.showtime.date.month == i]))
    elif period == 'month':
      this_year_month_bookings = [b for b in this_theater_bookings if (b.showtime.date.year == date.year and b.showtime.date.month == date.month)]
      for i in range(1, 32):
        result.append(len( [b for b in this_year_month_bookings if b.showtime.date.day == i]))
    else:
      week = date.isocalendar()[1]
      this_week_bookings = [b for b in this_theater_bookings if (b.showtime.date.year == date.year and b.showtime.date.isocalendar()[1] == week)]
      for i in range(1, 8):
        result.append(len([b for b in this_week_bookings if b.showtime.date.weekday() == i-1]))

    return Response(result)

class AdministrationAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsSystemAdmin]

  def create(self, request):
    serializer = AdministrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    theater = serializer.save()

    if not theater.image:
      image = Image.objects.create(
        data = DEFAULT_THEATER_IMAGE,
        kind = THEATER_IMAGE[0]
      )
      theater.image = image
      theater.save()

    return Response(data=serializer.data)

  def update(self, request, pk=None):
    theater = get_object_or_404(Theater, pk=pk)
    admins = [
      get_object_or_404(TheaterAdmin, pk=pk) for pk in request.data['admins']
    ]
    theater.admins.set(admins)
    theater.save()
    return Response(data=AdministrationSerializer(theater).data)

  def destroy(self, request, pk=None):
    theater = get_object_or_404(Theater, pk=pk)
    theater.delete()
    return Response(
      data={'message': 'Theater {0} successfully deleted.'.format(pk)}
    )

class AuditoriumAPI(ViewSet):
  permission_classes = [IsResponsibleForTheater]

  def list(self, request, theater_id=None):
    theater = get_object_or_404(Theater, id=theater_id)
    auditoriums = theater.auditoriums.all()
    return Response(AuditoriumSerializer(auditoriums, many=True).data)

  def retrieve(self, request, theater_id=None, pk=None):
    auditorium = get_object_or_404(Auditorium, id=pk)
    return Response(AuditoriumSerializer(auditorium).data)

  def create(self, request, theater_id=None):
    theater = get_object_or_404(Theater, id=theater_id)
    self.check_object_permissions(request, theater)
    request.data['theater'] = theater.id
    serializer = AuditoriumSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  def update(self, request, theater_id=None, pk=None):
    theater = get_object_or_404(Theater, id=theater_id)
    self.check_object_permissions(request, theater)
    auditorium = get_object_or_404(Auditorium, id=pk)
    request.data['theater'] = theater.id
    serializer = AuditoriumSerializer(auditorium, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    auditorium = serializer.save()
    return Response(data=serializer.data)

  def destroy(self, request, theater_id, pk):
    theater = get_object_or_404(Theater, pk=theater_id)
    self.check_object_permissions(request, theater)
    Auditorium.objects.get(id=pk).delete()
    return Response(data={'message': f'Auditorium {pk} successfully deleted.'})
