from django.db import models

from authentication.models import User
from showtimes.models import Showtime
from theaters.models import Theater

class TicketOnSale(models.Model):
  id = models.AutoField(primary_key=True)
  theater = models.ForeignKey(Theater, on_delete=models.PROTECT, related_name='tickets_on_sale')
  showtime = models.ForeignKey(Showtime, on_delete=models.PROTECT, related_name='tickets_on_sale')
  seat = models.IntegerField(blank=False)
  discount = models.IntegerField(blank=False)


class Booking(models.Model):
  id = models.AutoField(primary_key=True)
  showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, null=False, related_name='bookings')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
  discount = models.IntegerField(default=0)
  # price = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=300)
  # this will be foreign key soon
  seat = models.IntegerField(default=33)

  def price(self):
    return self.showtime.price