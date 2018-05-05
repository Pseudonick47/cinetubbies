from django.db import models

from fan_zone.props.models import Prop


class OfficialProp(Prop):
  quantity = models.IntegerField(
    blank=False,
    null=False
  )
  price = models.FloatField(
    blank=False,
    null=False
  )
  theater = models.ForeignKey(
    to='theaters.Theater',
    on_delete=models.CASCADE,
    related_name='officialprops'
  )
  category = models.ForeignKey(
    to='fan_zone.Category',
    on_delete=models.PROTECT,
    related_name='officialprops'
  )
