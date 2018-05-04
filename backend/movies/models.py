from django.db import models
from authentication.models import User
from theaters.models import Theater
from django.db.models import Count, Avg

class Movie(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=255, blank=False)
  genre = models.CharField(max_length=255, blank=False)
  director = models.CharField(max_length=255, blank=True)
  actors = models.CharField(max_length=255, blank=True)
  duration = models.CharField(max_length=255, blank=True)
  description = models.CharField(max_length=255, blank=True)
  theater = models.ForeignKey(Theater, on_delete=models.PROTECT, null=True, related_name='movies')
  voters = models.ManyToManyField(User, through='Voting', related_name='movie_voters')

  def get_all_votings(self):
    all_votes = {}
    for voter in self.voters.all():
      rating = Voting.objects.filter(user_id=voter.id, movie_id=self.id).get()
      all_votes[voter.id] = rating.rating
    return all_votes

  def get_voters_count(self):
    return self.voters.count()

  def get_avg_rating(self):
    rating = Voting.objects.filter(movie_id=self.id).aggregate(Avg('rating'))
    return rating['rating__avg']

  class Meta:
    db_table = 'movies'

class Voting(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='movie_voter')
  movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
  rating = models.IntegerField(default=0)
