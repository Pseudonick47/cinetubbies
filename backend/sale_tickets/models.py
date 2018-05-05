from django.db import models
from showtimes.models import Showtime
from theaters.models import Theater

class TicketOnSale(models.Model):
  id = models.AutoField(primary_key=True)
  theater = models.ForeignKey(Theater, on_delete=models.PROTECT, related_name='tickets_on_sale')
  showtime = models.ForeignKey(Showtime, on_delete=models.PROTECT, related_name='tickets_on_sale')
  seat = models.IntegerField(blank=False)
  discount = models.IntegerField(blank=False)
