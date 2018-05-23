from django.db import models
from movies.models import Movie
from theaters.models import Auditorium

class Showtime(models.Model):
  id = models.AutoField(primary_key=True)
  auditorium = models.ForeignKey(Auditorium, on_delete=models.PROTECT, null=True, related_name='showtimes')
  date = models.DateField(blank=False)
  time = models.TimeField(blank=False)
  price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
  movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=True, related_name='showtimes')

  def seats(self):
    seats = self.bookings.all().values('user_id', 'seat')
    layout = []
    index = 0
    for seat in seats:
      (x, y) = divmod(index, len(self.auditorium.layout['layout'][0]))
      layout.append({
        'taken': 1 if self.auditorium.layout['layout'][x][y] == 0 or seat['user_id'] else 0,
        'seat': seat['seat']
      })
      index += 1
    return layout
