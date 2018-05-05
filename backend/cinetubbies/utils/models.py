from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OptimisticLockingModel(models.Model):
  id = models.AutoField(primary_key=True)
  version = models.IntegerField()

  def save(self, *args, **kwargs):
    try:
      self.objects.filter(id=self.id, version=self.version).get()
      self.version += 1
      super().save(*args, **kwargs)

    except ObjectDoesNotExist:
      raise ObjectLocked

  class Meta:
    abstract = True


class ObjectLocked(Exception):
  pass