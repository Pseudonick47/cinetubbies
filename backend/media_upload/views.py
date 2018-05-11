from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


from authentication.permissions import IsAdmin

from .models import Image
from .serializers import ImageSerializer


class PublicAPI(ViewSet):
  permission_classes = [AllowAny]

  def list(self, request):
    images = Image.objects.all()
    return Response(data=ImageSerializer(images, many=True).data)

  def retrieve(self, request, pk=None):
    image = get_object_or_404(Image, pk=pk)
    return Response(data=ImageSerializer(image).data)


class MemberAPI(ViewSet):
  permission_classes = [IsAuthenticated]

  def create(self, request):
    serializer = ImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  def update(self, request, pk=None):
    image = get_object_or_404(Image, pk=pk)
    serializer = ImageSerializer(image, data=request, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  def destroy(self, request, pk=None):
    image = get_object_or_404(Image, pk=pk)
    image.delete()
    return Response(
      data={'message': 'Image {0} successfully deleted.'.format(pk)}
    )
