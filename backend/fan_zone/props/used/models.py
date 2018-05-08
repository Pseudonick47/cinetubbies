from django.db import models
from cinetubbies.utils.models import OptimisticLockingModel

from fan_zone.props.models import Prop


class UsedProp(Prop, OptimisticLockingModel):
  id = models.AutoField(primary_key=True)
  owner = models.ForeignKey(
    to='authentication.User',
    on_delete=models.CASCADE,
    null=False,
    related_name='usedprops'
  )
  category = models.ForeignKey(
    to='fan_zone.Category',
    on_delete=models.PROTECT,
    related_name='usedprops'
  )
  post_date = models.DateField(auto_now_add=True)
  expiration_date = models.DateField()
  approved = models.BooleanField(default=False)
  pending_approval = models.BooleanField(default=True)
