from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import TheaterAdmin

from .models import Theater, THEATER_KIND, Voting
from .serializers import PublicSerializer
from .serializers import RestrictedSerializer
from .serializers import AdministrationSerializer
from .permissions import IsResponsibleForTheater
from .permissions import IsTheaterOrSystemAdmin
from .permissions import IsSystemAdmin


class PublicAPI(ViewSet):
  queryset = Theater.objects.all()
  permission_classes = [AllowAny]

  def list(self, request):
    num = request.GET.get('num')
    paginator = Paginator(self.queryset.order_by('name'), num if num else 10)
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
    return Response(data=PublicSerializer(self.queryset, many=True).data)

  @action(detail=False)
  def update_rating(self, request):
    vote, _ = Voting.objects.get_or_create(
      user_id=request.user.id,
      theater_id=request.data['id']
    )
    vote.rating = request.data['rating']
    vote.save()
    rating = Voting.objects.filter(
      theater_id=request.data['id']).aggregate(rating=Avg('rating')
    )
    voters = len(Voting.objects.filter(theater_id=request.data['id']).all())
    data = {'rating':rating,'voters':voters}
    return Response(data)


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

class AdministrationAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsSystemAdmin]

  def create(self, request):
    serializer = AdministrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
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
