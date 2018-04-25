from django.db import models
from django.shortcuts import get_object_or_404

from authentication.models import User
from django.db.models import Count, Avg


THEATER_KIND = [
    ('p', 'Play'),
    ('m', 'Movie'),
]

class Theater(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    admin = models.ForeignKey(User, on_delete=models.PROTECT, related_name='admin')
    kind = models.CharField(
        max_length=1, choices=THEATER_KIND
    )
    voters = models.ManyToManyField(User, through='Voting', related_name='voters')

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
        return '{0} {1}, {2} theater'.format(self.id, self.name, self.kind)

class Voting(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    theater = models.ForeignKey(Theater, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)