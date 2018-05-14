from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from fan_zone.categories.models import Category
from fan_zone.categories.serializers import PublicSerializer as \
                                            CategorySerializer

from fan_zone.props.models import Prop
from fan_zone.props.serializers import PropSerializer

from media_upload.models import Image
from media_upload.serializers import ImageSerializer


class PublicAPI(ViewSet):
  permission_classes = [AllowAny]

  @action(detail=False)
  def count(self, request, *args, **kwargs):
    category_id = request.GET.get('category')

    queryset = Prop.objects.all()

    if category_id:
      queryset = queryset.filter(category_id=category_id)

    return Response(data=queryset.count())

  def list(self, request, *args, **kwargs):
    category_id = request.GET.get('category')

    queryset = Prop.objects.all()

    if category_id:
      queryset = queryset.filter(category_id=category_id)

    num = request.GET.get('num') or 10
    paginator = Paginator(queryset.order_by('title'), num)
    page = request.GET.get('num') or 1
    props = paginator.get_page(page).object_list

    return Response(data=PropSerializer(props, many=True).data)

  def retrieve(self, request, *args, **kwargs):
    pk = kwargs.pop('pk')
    prop = get_object_or_404(Prop, pk=pk)
    return Response(data=PropSerializer(prop).data)
