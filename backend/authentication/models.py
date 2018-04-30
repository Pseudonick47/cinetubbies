from django.db import models
from django.db.models import Q
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
  friendships = models.ManyToManyField('self', through='Friendship', symmetrical=False)

  def friend_requests(self):
    requests_ids = Friendship.objects.filter(friend_id=self.id).filter(accepted=False).values_list('me_id')
    return User.objects.filter(id__in=requests_ids)

  def friends(self):
    they_added = Friendship.objects.filter(friend_id=self.id).filter(accepted=True).values_list('me_id')
    i_added = Friendship.objects.filter(me_id=self.id).filter(accepted=True).values_list('friend_id')
    return User.objects.filter(Q(id__in=i_added) | Q(id__in=they_added))

  def friends_count(self):
    friends.count()


class Friendship(models.Model):
    me = models.ForeignKey(User, on_delete=models.PROTECT, related_name='me')
    friend = models.ForeignKey(User, on_delete=models.PROTECT, related_name='friend')
    accepted = models.BooleanField(default=False)
