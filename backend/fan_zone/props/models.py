from django.db import DatabaseError
from django.db import models
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from cinetubbies.utils.models import ObjectLocked



OFFICIAL_PROP = ('O', 'Official')
USED_PROP = ('U', 'Used')
PROP_KIND = (
  OFFICIAL_PROP,
  USED_PROP
)


class AbstractProp(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True, default='')
  image = models.ForeignKey(
    to="media_upload.Image",
    on_delete=models.SET_NULL,
    related_name='+',
    null=True
  )
  category = models.ForeignKey(
    to='fan_zone.Category',
    on_delete=models.PROTECT,
    related_name='+'
  )
  post_date = models.DateField(auto_now_add=True)

  class Meta:
    abstract = True


class OfficialProp(models.Model):
  quantity = models.PositiveSmallIntegerField(
    null=True
  )
  price = models.FloatField(
    null=True
  )
  theater = models.ForeignKey(
    to='theaters.Theater',
    on_delete=models.CASCADE,
    related_name='+',
    null=True
  )

  class Meta:
    abstract = True


class OfficialPropManager(models.Manager):

  def get_queryset(self):
    return super().get_queryset().filter(kind=OFFICIAL_PROP[0])


class UsedProp(models.Model):
  owner = models.ForeignKey(
    to='authentication.User',
    on_delete=models.CASCADE,
    null=True,
    related_name='+'
  )
  expiration_date = models.DateField(
    null=True
  )
  approved = models.BooleanField(default=False)
  pending_approval = models.BooleanField(default=True)

  class Meta:
    abstract = True


class UsedPropManager(models.Manager):

  def get_queryset(self):
    return super().get_queryset().filter(kind=USED_PROP[0])


class Prop(AbstractProp, OfficialProp, UsedProp):
  id = models.AutoField(
    primary_key=True
  )
  kind = models.CharField(
    max_length=1,
    choices=PROP_KIND,
  )
  version = models.IntegerField(
    default=1
  )
  objects = models.Manager()
  official = OfficialPropManager()
  used = UsedPropManager()

  @transaction.atomic
  def save(self, *args, **kwargs):
      queryset = Prop.objects.select_for_update()
      #lock object
      try:
        queryset.filter(id=self.id, version=self.version).get()
      except DatabaseError:
        raise ObjectLocked
      except ObjectDoesNotExist:
        pass

      if self.kind == OFFICIAL_PROP[0]:
        if self.quantity < 0:
          raise ValueError('Quantity can\'t be less then 0.')

      self.version += 1
      super().save(*args, **kwargs)

