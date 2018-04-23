from django.db import models
from authentication.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False)
    genre = models.CharField(max_length=255, blank=False)
    director = models.CharField(max_length=255, blank=True)
    actors = models.CharField(max_length=255, blank=True)
    duration = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    admin = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'movies'
