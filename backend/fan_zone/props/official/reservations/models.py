from django.db import models


class Reservation(models.Model):
  id = models.AutoField(
    primary_key=True
  )
  user = models.ForeignKey(
    to='authentication.User',
    on_delete=models.CASCADE,
    related_name='prop_reservations'
  )
  prop = models.ForeignKey(
    to='fan_zone.Prop',
    on_delete=models.CASCADE,
    related_name='+'
  )
  quantity = models.PositiveSmallIntegerField()
