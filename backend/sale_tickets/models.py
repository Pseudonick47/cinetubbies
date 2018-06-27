from django.db import models

from authentication.models import User
from showtimes.models import Showtime
from theaters.models import Theater
from django.db import DatabaseError
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from cinetubbies.utils.models import ObjectLocked

class TicketOnSale(models.Model):
  id = models.AutoField(primary_key=True)
  theater = models.ForeignKey(Theater, on_delete=models.PROTECT, related_name='tickets_on_sale')
  showtime = models.ForeignKey(Showtime, on_delete=models.PROTECT, related_name='tickets_on_sale')
  seat = models.IntegerField(blank=False)
  discount = models.IntegerField(blank=False)
  deleted = models.IntegerField(blank=False, default=0)


class Booking(models.Model):
  id = models.AutoField(primary_key=True)
  showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, null=False, related_name='bookings')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True)
  discount = models.IntegerField(default=0)
  seat = models.IntegerField(default=0)
  version = models.IntegerField(
    default=1
  )

  def price(self):
    return self.showtime.price

  def get_discount(self):
    return self.discount * self.showtime.price / 100

  def date(self):
    return self.showtime.date

  def getTheater(self):
    return self.showtime.movie.theater

  def get_user(self):
    return self.user

  @transaction.atomic
  def save(self, *args, **kwargs):
      queryset = Booking.objects.select_for_update()
      #lock object
      try:
        queryset.filter(id=self.id, version=self.version).get()
      except DatabaseError:
        raise ObjectLocked
      except ObjectDoesNotExist:
        pass

      self.version += 1
      super().save(*args, **kwargs)

