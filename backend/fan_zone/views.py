from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.permissions import IsFanZoneOrSystemAdmin
from authentication.permissions import IsSystemAdmin

from media_upload.defaults import DEFAULT_PROP_IMAGE
from media_upload.models import Image
from media_upload.models import OFFICIAL_PROP_IMAGE

from theaters.models import Theater

from .models import OfficialProp
from .models import Category
from .permissions import IsResponsibleForOfficialProp
from .serializers import AdminCategorySerializer
from .serializers import PublicCategorySerializer
from .serializers import PublicOfficialPropSerializer
from .serializers import RestrictedOfficialPropSerializer



class PublicOfficialPropAPI(ViewSet):
  permission_classes = [AllowAny]

  def list(self, request, theater_pk=None, category_pk=None):
    queryset = OfficialProp.objects.all()

    if theater_pk:
      get_object_or_404(Theater, pk=theater_pk)
      queryset = OfficialProp.objects.filter(theater_id=theater_pk)

    if category_pk:
      get_object_or_404(Category, pk=category_pk)
      queryset = queryset.filter(category_id=category_pk)

    num = request.GET.get('num')
    paginator = Paginator(queryset.order_by('title'), num if num else 10)
    page = request.GET.get('page')

    props = paginator.get_page(page if page else 1)
    return Response(data=PublicOfficialPropSerializer(props, many=True).data)

  def retrieve(self, request, theater_pk=None, category_pk=None, pk=None):
    prop = get_object_or_404(OfficialProp, pk=pk)
    return Response(data=PublicOfficialPropSerializer(prop).data)

  @action(detail=False)
  def count(self, request, theater_pk=None, category_pk=None):
    queryset = OfficialProp.objects.all()

    if theater_pk:
      get_object_or_404(Theater, pk=theater_pk)
      queryset = queryset.filter(theater_id=theater_pk)

    if category_pk:
      get_object_or_404(Category, pk=category_pk)
      queryset = queryset.filter(category_id=category_pk)

    return Response(data=queryset.count())

class RestrictedOfficialPropAPI(ViewSet):
  permission_classes = [
    IsAuthenticated, IsFanZoneOrSystemAdmin, IsResponsibleForOfficialProp
  ]

  def create(self, request, theater_pk=None):
    serializer = RestrictedOfficialPropSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    prop = serializer.save()

    if not prop.image:
      image = Image.objects.create(
        path = DEFAULT_PROP_IMAGE,
        kind = OFFICIAL_PROP_IMAGE[0]
      )
      prop.image = image
      prop.save()

    return Response(data=serializer.data)

  def destroy(self, request, theater_pk=None, pk=None):
    prop = get_object_or_404(OfficialProp, pk=pk)
    self.check_object_permissions(request, prop)
    prop.delete()
    return Response(
      data={'message': 'Official prop {0} successfully deleted.'.format(pk)}
    )

  def update(self, request, theater_pk=None, pk=None):
    prop = get_object_or_404(OfficialProp, pk=pk)
    self.check_object_permissions(request, prop)
    serializer = RestrictedOfficialPropSerializer(
      prop, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

class PublicCategoryAPI(ViewSet):
  permission_classes = [AllowAny]

  def list(self, request):
    categories = Category.objects.all()
    return Response(data=PublicCategorySerializer(categories, many=True).data)

  def retrieve(self, request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    return Response(data=PublicCategorySerializer(category).data)

class AdminCategoryAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsSystemAdmin]

  def create(self, request):
    serializer = AdminCategorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  def destroy(self, request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return Response(
      data={'message': 'Category {0} successfully deleted.'.format(pk)}
    )

  def update(self, request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    serializer = AdminCategorySerializer(
      category, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)
