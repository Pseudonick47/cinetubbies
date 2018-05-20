from django.db import models


class Offer(models.Model):
  id = models.AutoField(
    primary_key=True
  )
  user = models.ForeignKey(
    to='authentication.User',
    on_delete=models.CASCADE,
    related_name='prop_offers'
  )
  prop = models.ForeignKey(
    to='fan_zone.Prop',
    on_delete=models.CASCADE,
    related_name='+'
  )
  sum = models.PositiveIntegerField()
