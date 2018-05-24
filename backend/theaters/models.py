from django.db import models
from django.shortcuts import get_object_or_404
from authentication.models import User
from django.db.models import Avg
from django.db.models.signals import post_init, pre_save, post_save
import json
from django.core.serializers import serialize


THEATER_KIND = [
  ('p', 'Play'),
  ('m', 'Movie'),
]


class Theater(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=300)
  description = models.TextField(blank=True, default='')
  kind = models.CharField(
    max_length=1, choices=THEATER_KIND
  )
  voters = models.ManyToManyField(User, through='Voting', related_name='voters')
  image = models.ForeignKey(to="media_upload.Image", on_delete=models.SET_NULL, related_name='+', null=True)
  lat = models.DecimalField(blank=True, decimal_places=15, max_digits=20, null=True)
  lng = models.DecimalField(blank=True, decimal_places=15, max_digits=20, null=True)

  def get_all_votings(self):
    all_votes = {}
    for voter in self.voters.all():
      rating = Voting.objects.filter(user_id=voter.id, theater_id=self.id).get()
      all_votes[voter.id] = rating.rating
    return all_votes

  def get_voters_count(self):
    return self.voters.count()

  def get_avg_rating(self):
    rating = Voting.objects.filter(theater_id=self.id).aggregate(Avg('rating'))
    return rating['rating__avg']

  def __str__(self):
    return serialize('json', [self])[1:-1]

  def __eq__(self, other):
    if not isinstance(other, Theater):
      return False
    return self.id == other.id


class Voting(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  theater = models.ForeignKey(Theater, on_delete=models.PROTECT)
  rating = models.IntegerField(default=0)

class Auditorium(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=100, blank=False)
  layout = models.TextField()
  theater = models.ForeignKey(to='theaters.Theater', on_delete=models.SET_NULL, related_name='auditoriums', null=True)

def layout_to_dict(**kwargs):
  instance = kwargs.get('instance')
  if type(instance.layout).__name__=='str':
    instance.layout = json.loads(instance.layout)

def layout_to_str(sender, instance, **kwargs):
  instance.layout = json.dumps(instance.layout)

post_init.connect(layout_to_dict, sender=Auditorium)
pre_save.connect(layout_to_str, Auditorium)
post_save.connect(layout_to_dict, Auditorium)
