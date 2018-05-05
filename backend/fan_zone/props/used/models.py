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
  post_date = models.DateTimeField(auto_now_add=True)
  expiration_date = models.DateTimeField()
  approved = models.BooleanField(default=False)
  pending_approval = models.BooleanField(default=True)
