from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from fan_zone.categories.models import Category

from fan_zone.props.serializers import PropSerializer
from fan_zone.props.official.models import OfficialProp
from fan_zone.props.used.models import UsedProp


class PublicAPI(ViewSet):

  @action(detail=False)
  def count(self, request, *args, **kwargs):
    category_id = request.GET.get('category')

    official = OfficialProp.objects

    if category_id:
      get_object_or_404(Category, pk=category_id)
      official = official.filter(category_id=category_id)
    used = UsedProp.objects.filter(approved=True)

    if category_id:
      used = used.filter(category_id=category_id)

    return Response(data=official.count() + used.count())

  def list(self, request, *args, **kwargs):
    category_id = request.GET.get('category')

    fields = ['id', 'title', 'description', 'image_id', 'post_date']

    official = OfficialProp.objects.all()

    if category_id:
      get_object_or_404(Category, pk=category_id)
      official = official.filter(category_id=category_id)

    official = official.values(*fields)

    used = UsedProp.objects.filter(approved=True)

    if category_id:
      used = used.filter(category_id=category_id)

    used = used.values(*fields)

    num = request.GET.get('num') or 10
    paginator = Paginator(official.union(used).order_by('title'), num)
    page = request.GET.get('num') or 1
    props = paginator.get_page(page)

    return Response(data=PropSerializer(props, many=True).data)
