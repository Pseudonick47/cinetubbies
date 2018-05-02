from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.permissions import IsSystemAdmin

from .models import RewardScale
from .serializers import RewardScaleSerializer


class RewardScaleAPI(ViewSet):
  permission_classes = [IsAuthenticated, IsSystemAdmin]

  def list(self, request):
    scales = RewardScale.objects.all()
    return Response(data=RewardScaleSerializer(scales, many=True).data)

  def retrieve(self, request, pk=None):
    scale = get_object_or_404(RewardScale, pk=pk)
    return Response(data=RewardScaleSerializer(scale).data)

  def update(self, request, pk=None):
    scale = get_object_or_404(RewardScale, pk=pk)
    serializer = RewardScaleSerializer(scale, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)

  @action(detail=False)
  def update_all(self, request):
    res = []
    for obj in request.data:
      scale = get_object_or_404(RewardScale, pk=obj['status'])
      serializer = RewardScaleSerializer(scale, data=obj, partial=True)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      res.append(serializer.data)
    return Response(data=res)
