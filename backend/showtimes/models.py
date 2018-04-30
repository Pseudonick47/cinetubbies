from django.db import models
from movies.models import Movie

class Showtime(models.Model):
  id = models.AutoField(primary_key=True)
  auditorium = models.CharField(max_length=255, blank=False)
  date = models.DateField(blank=False)
  time = models.TimeField(blank=False)
  price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
  movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=True, related_name='showtimes')
