from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.permissions import IsFanZoneOrSystemAdmin
from authentication.permissions import IsSystemAdmin

from .models import OfficialProp
from .models import Category
from .permissions import IsResponsibleForOfficialProp
from .serializers import AdminCategorySerializer
from .serializers import PublicCategorySerializer
from .serializers import PublicOfficialPropSerializer
from .serializers import RestrictedOfficialPropSerializer



class PublicOfficialPropAPI(ViewSet):
  queryset = OfficialProp.objects.all()
  permission_classes = [AllowAny]

  def list(self, request):
    num = request.GET.get('num')
    paginator = Paginator(self.queryset.order_by('title'), num if num else 10)
    page = request.GET.get('page')
    props = paginator.get_page(page if page else 1)
    return Response(data=PublicOfficialPropSerializer(props, many=True).data)

  def retrieve(self, request, pk=None):
    prop = get_object_or_404(OfficialProp, pk=pk)
    return Response(data=PublicOfficialPropSerializer(prop).data)

  @action(detail=False)
  def count(self, request):
    return Response(data=OfficialProp.objects.count())

class RestrictedOfficialPropAPI(ViewSet):
  permission_classes = [
    IsAuthenticated, IsFanZoneOrSystemAdmin, IsResponsibleForOfficialProp
  ]

  def create(self, request):
    serializer = RestrictedOfficialPropSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  def destroy(self, request, pk=None):
    prop = get_object_or_404(OfficialProp, pk=pk)
    self.check_object_permissions(request, prop)
    prop.delete()
    return Response(
      data={'message': 'Official prop {0} successfully deleted.'.format(pk)}
    )

  def update(self, request, pk=None):
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

  def delete(self, request, pk=None):
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
