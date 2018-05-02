from django.db import models


BASIC = ('basic', 'Basic')
BRONZE = ('bronze', 'Bronze')
SILVER = ('silver', 'Silver')
GOLD = ('gold', 'Gold')

REWARD_STATUS = (
  BASIC,
  BRONZE,
  SILVER,
  GOLD
)


class RewardScale(models.Model):
  status = models.CharField(
    primary_key=True,
    max_length=6,
    choices=REWARD_STATUS
  )
  min_points = models.PositiveSmallIntegerField(blank=False)
  max_points = models.PositiveSmallIntegerField(blank=False)
