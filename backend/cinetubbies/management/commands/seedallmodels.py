from django.db import transaction
from django.core.management.base import BaseCommand

from authentication.serializers import UserSerializer
from authentication.serializers import AdminSerializer
from authentication.serializers import TheaterAdminSerializer

from theaters.serializers import AdministrationSerializer
from movies.serializers import MovieSerializer
from showtimes.serializers import ShowtimeSerializer
from theaters.serializers import PublicSerializer
from theaters.serializers import AuditoriumSerializer

from fan_zone.categories.serializers import AdministrationSerializer as CategorySerializer
from fan_zone.props.official.serializers import RestrictedSerializer as OPropSerializer
from fan_zone.props.used.serializers import MemberSerializer as UPropSerializer

import sys

class Command(BaseCommand):
  help = 'Seed all tables in the database with dummy data'

  def handle(self, *args, **options):
    try:
      with transaction.atomic():
        seed()
      self.stdout.write(self.style.SUCCESS('DB seed finished successfully'))
    except Exception as e:
      self.stdout.write(self.style.ERROR('DB seed failed \n' + str(e)))

def seed():
  for admin in system_admins:
    serializer = AdminSerializer(data=admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for admin in theater_admins:
    serializer = TheaterAdminSerializer(data=admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for admin in fan_zone_admins:
    serializer =AdminSerializer(data=admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for user in users:
    serializer = UserSerializer(data=user)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for theater in theaters:
    serializer = AdministrationSerializer(data=theater)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for auditorium in auditoriums:
    serializer = AuditoriumSerializer(data=auditorium)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for movie in movies:
    serializer = MovieSerializer(data=movie, partial=True)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for showtime in showtimes:
    serializer = ShowtimeSerializer(data=showtime, partial=True)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for category in categories:
    serializer = CategorySerializer(data=category, partial=True)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for prop in officialprops:
    serializer = OPropSerializer(data=prop, partial=True)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  for prop in usedprops:
    serializer = UPropSerializer(data=prop, partial=True)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

users = [
  {
    'username': 'user1',
    'first_name': 'Njegomir',
    'password': '123456',
    'phone': '12312',
    'city': 'Cetinje',
    'role': 'user',
    'email': 'user1@test.com',
  },
  {
    'username': 'user2',
    'first_name': 'user',
    'password': '123456',
    'phone': '12312',
    'city': 'Novi Sad',
    'role': 'user',
    'email': 'user2@test.com',
  },
  {
    'username': 'user3',
    'first_name': 'Third',
    'password': '123456',
    'phone': '12312',
    'city': 'Odzaci',
    'role': 'user',
    'email': 'user3@test.com',
  }
]

theater_admins = [
  {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  },
  {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }
]

fan_zone_admins = [
  {
    'username': 'admin3',
    'password': '123456',
    'email': 'admin3@test.com',
    'role': 'fan_zone_admin',
    'theater': '',
  }
]

system_admins = [
  {
    'username': 'sysadmin',
    'password': '123456',
    'role': 'admin',
    'email': 'sysadmin@test.com',
  }
]

theaters = [
  {
    'name': 'Theater first',
    'address': 'Boulevard of Broken Dreams',
    'kind': 'p',
    'admins': [3],
  },
  {
    'name': 'Theater second',
    'address': 'Highway to Hell',
    'kind': 'p',
    'admins': [2],
  }
]

auditoriums = [
  {
    'name': 'Mala sala',
    'layout': '{"layout": [[0, 0, 0], [1, 1, 0], [1, 1, 1]]}',
    'theater': 1
  },
  {
    'name': 'Velika sala',
    'layout': '{"layout": [[0, 0, 0], [1, 1, 0], [1, 1, 1]]}',
    'theater': 1
  },
  {
    'name': 'Srednja sala',
    'layout': '{"layout": [[0, 0, 0], [1, 1, 0], [1, 1, 1]]}',
    'theater': 1
  }
]

movies = [
  {
    'title': 'The Fate of the Furious',
    'genre': 'Action',
    'director': 'F. Gary Gray',
    'actors': 'Vin Diesel, Jason Statham, Dwayne Johnson',
    'duration': '2h 16min ',
    'description': 'When a mysterious woman seduces Dom into the world of terrorism and a betrayal of those closest to him, the crew face trials that will test them as never before.',
    'theater': 1
  }
]

showtimes = [
  {
    'auditorium': 1,
    'date': '2018-05-16',
    'time': '01:10:00',
    'price': 400,
    'movie': 1
  },
  {
    'auditorium': 2,
    'date': '2018-05-19',
    'time': '01:10:00',
    'price': 400,
    'movie': 1
  },
  {
    'auditorium': 1,
    'date': '2018-05-19',
    'time': '18:00:00',
    'price': 400,
    'movie': 1
  },
  {
    'auditorium': 2,
    'date': '2018-05-19',
    'time': '19:00:00',
    'price': 500,
    'movie': 1
  },
  {
    'auditorium': 3,
    'date': '2018-05-14',
    'time': '12:45:00',
    'price': 200,
    'movie': 1
  }
]

categories = [
  {
    'name': 'cat',
    'supercategory': None
  },
  {
    'name': 'subcat1',
    'supercategory': 1
  },
  {
    'name': 'subcat1',
    'supercategory': 1
  },
  {
    'name': 'subsubcat1',
    'supercategory': 3
  },
  {
    'name': 'cat2',
    'supercategory': None
  },
  {
    'name': 'subcat3',
    'supercategory': 5
  }
]

officialprops = [
  {
    'title': 'Prop1',
    'description': 'some profound text here',
    'categoryId': 3,
    'quantity': 2,
    'price': 99.9,
    'theaterId': 1,
    'imageId': None,
    'kind': 'O'
  },
  {
    'title': 'Prop2',
    'description': 'some profound text here',
    'categoryId': 3,
    'quantity': 2,
    'price': 99.9,
    'theaterId': 1,
    'imageId': None,
    'kind': 'O'
  },
  {
    'title': 'Prop3',
    'description': 'some profound text here',
    'categoryId': 3,
    'quantity': 2,
    'price': 99.9,
    'theaterId': 1,
    'imageId': None,
    'kind': 'O'
  },
  {
    'title': 'Prop4',
    'description': 'some profound text here',
    'categoryId': 3,
    'quantity': 10,
    'price': 99.9,
    'theaterId': 1,
    'imageId': None,
    'kind': 'O'
  },
]

usedprops = [
  {
    'title': 'Prop1',
    'description': 'some profound text here',
    'ownerId': 5,
    'categoryId': 1,
    'imageId': None,
    'expirationDate': '2018-06-01',
    'kind': 'U'
  },
  {
    'title': 'Prop2',
    'description': 'some profound text here',
    'ownerId': 5,
    'categoryId': 1,
    'imageId': None,
    'expirationDate': '2018-06-01',
    'kind': 'U'
  },
  {
    'title': 'Prop3',
    'description': 'some profound text here',
    'ownerId': 6,
    'categoryId': 1,
    'imageId': None,
    'expirationDate': '2018-06-01',
    'kind': 'U'
  }
]