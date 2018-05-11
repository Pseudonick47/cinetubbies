from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.permissions import IsSystemAdmin

from .models import Category
from .serializers import PublicSerializer
from .serializers import AdministrationSerializer


class PublicAPI(ViewSet):
  permission_classes = [AllowAny]

  def list(self, request):
    categories = Category.objects.all()
    return Response(data=PublicSerializer(categories, many=True).data)

  def retrieve(self, request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    return Response(data=PublicSerializer(category).data)


class AdministrationAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsSystemAdmin]

  def create(self, request):
    serializer = AdministrationSerializer(data=request.data)
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
    serializer = AdministrationSerializer(
      category, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)