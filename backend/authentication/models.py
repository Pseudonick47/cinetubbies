from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize


SYSTEM_ADMIN = ('admin', 'Admin')
THEATER_ADMIN = ('cinema_admin', 'Theater Admin')
FAN_ZONE_ADMIN = ('fan_zone_admin', 'Fan Zone Admin')
USER = ('user', 'User')

ADMIN_ROLES = (
  SYSTEM_ADMIN,
  THEATER_ADMIN,
  FAN_ZONE_ADMIN,
)

ROLES = ADMIN_ROLES + (USER,)


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
  first_login = models.BooleanField(default=True)
  image = models.ForeignKey(to="media_upload.Image", on_delete=models.SET_NULL, related_name='+', null=True)

  def is_admin(self):
    return self.role in [admin[0] for admin in ADMIN_ROLES]

  def is_system_admin(self):
    return self.role == SYSTEM_ADMIN[0]

  def is_theater_admin(self):
    return self.role == THEATER_ADMIN[0]

  def is_fan_zone_admin(self):
    return self.role == FAN_ZONE_ADMIN[0]

  def friend_requests(self):
    requests_ids = Friendship.objects.filter(friend_id=self.id).filter(accepted=False).values_list('me_id')
    return User.objects.filter(id__in=requests_ids)

  def friends(self):
    they_added = Friendship.objects.filter(friend_id=self.id).filter(accepted=True).values_list('me_id')
    i_added = Friendship.objects.filter(me_id=self.id).filter(accepted=True).values_list('friend_id')
    return User.objects.filter(Q(id__in=i_added) | Q(id__in=they_added))

  def friends_count(self):
    self.friends().count()


class Friendship(models.Model):
    me = models.ForeignKey(User, on_delete=models.PROTECT, related_name='me')
    friend = models.ForeignKey(User, on_delete=models.PROTECT, related_name='friend')
    accepted = models.BooleanField(default=False)


class TheaterAdmin(User):
  theater = models.ForeignKey(
    to='theaters.Theater',
    on_delete=models.SET_NULL,
    related_name='theateradmins',
    null=True,
  )

  def __str__(self):
    return serialize('json', [self])[1:-1]

class FanZoneAdmin(User):
  theater = models.ForeignKey(
    to='theaters.Theater',
    on_delete=models.SET_NULL,
    related_name='fanzoneadmins',
    null=True,
  )

  def __str__(self):
    return serialize('json', [self])[1:-1]
