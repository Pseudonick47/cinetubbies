from django.db import models
from django.shortcuts import get_object_or_404

from authentication.models import User


THEATER_KIND = [
    ('p', 'Play'),
    ('m', 'Movie'),
]

class Theater(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    admin = models.ForeignKey(User, on_delete=models.PROTECT)
    kind = models.CharField(
        max_length=1, choices=THEATER_KIND
    )
