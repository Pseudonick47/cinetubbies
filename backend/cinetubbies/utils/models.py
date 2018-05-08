from django.db import DatabaseError
from django.db import models
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


class OptimisticLockingModel(models.Model):
  id = models.AutoField(primary_key=True)
  version = models.IntegerField(default=1)

  @transaction.atomic
  def save(self, *args, **kwargs):
      queryset = self.__class__.objects.select_for_update()
      #lock object
      try:
        queryset.filter(id=self.id, version=self.version).get()
      except DatabaseError:
        raise ObjectLocked
      except ObjectDoesNotExist:
        pass

      self.version += 1
      print(self.__dict__)
      super().save(*args, **kwargs)

  class Meta:
    abstract = True


class ObjectLocked(Exception):
  pass