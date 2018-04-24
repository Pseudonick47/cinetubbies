from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    ('admin', 'Admin'),
    ('cinema_admin', 'Cinema Admin'),
    ('fan_zone_admin', 'FanZone Admin'),
    ('user', 'User')
  )

class User(AbstractUser):
  id = models.AutoField(primary_key=True)
  username = models.CharField(max_length=30, unique=True, editable=False)
  password = models.CharField(max_length=255)
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=30, blank=True)
  birth_date = models.DateField(null=True, blank=True)
  role = models.CharField(max_length=20, choices=ROLES, default='user')
  phone = models.CharField(max_length=30, blank=True)
  city = models.CharField(max_length=30, blank=True)
  friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)


class Friendship(models.Model):
    me = models.ForeignKey(User, on_delete=models.PROTECT, related_name='me')
    friend = models.ForeignKey(User, on_delete=models.PROTECT, related_name='friend')
    accepted = models.BooleanField(default=False)
