from collections import Counter
from rest_framework.test import APITestCase

from authentication.models import User
from authentication.serializers import TheaterAdminSerializer
from authentication.serializers import AdminSerializer

from theaters.models import Theater
from theaters.serializers import AdministrationSerializer
from theaters.serializers import PublicSerializer

from showtimes.models import Showtime
from showtimes.serializers import ShowtimeSerializer

from .models import Movie
from .serializers import MovieSerializer

class MovieAPITests(APITestCase):
  test_theater_admin = {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_theater_admin2 = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_fan_zone_admin = {
    'username': 'admin3',
    'password': '123456',
    'email': 'admin3@test.com',
    'role': 'fan_zone_admin',
  }

  test_system_admin = {
    'username': 'sysadmin',
    'password': '123456',
    'role': 'admin',
    'email': 'sysadmin@test.com',
  }

  test_user = {
    'username': 'username',
    'password': '123456',
    'phone': '123',
    'city': 'city'
  }

  test_theater = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'admins': [1],
  }

  test_theater2 = {
    'name': 'theater2',
    'address': 'address',
    'kind': 'm',
    'admins': [2],
  }

  test_movie = {
    'title': 'title',
    'genre': 'genre',
    'theater': 1
  }

  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_fan_zone_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_system_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_user)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdministrationSerializer(data=self.test_theater)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdministrationSerializer(data=self.test_theater2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = MovieSerializer(data=self.test_movie)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def login(self, user):
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': user['username'],
        'password': user['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

  def post(self, new_movie):
    return self.client.post(
      path='http://localhost:8000/api/movies/',
      data = new_movie,
      format='json'
    )

  def delete(self, id):
    return self.client.delete(
      path='http://localhost:8000/api/movies/'+id+'/'
    )

  def get(self, id):
    return self.client.get(
      path='http://localhost:8000/api/movies/'+id+'/'
    )

  def put(self, movie, id):
    return self.client.put(
      path='http://localhost:8000/api/movies/'+id+'/',
      data = movie,
      format='json'
    )

  def test_create(self):
    new_movie = {
      'title': 'title',
      'genre': 'genre',
      'director': '',
      'actors': '',
      'duration': '',
      'description': '',
      'theater': 1
    }

    # login and post as a user; fail
    self.login(self.test_user)
    response = self.post(new_movie)
    self.assertEqual(response.status_code, 403)

    # login and post as a system admin; fail
    self.login(self.test_system_admin)
    response = self.post(new_movie)
    self.assertEqual(response.status_code, 403)

    # login and post as a theater admin; pass
    self.login(self.test_theater_admin)
    response = self.post(new_movie)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(Movie.objects.all().count() == 2)

    # non-existing theater; fail
    new_movie['theater'] = 3
    response = self.post(new_movie)
    self.assertEqual(response.status_code, 400)

    # no title; fail
    new_movie['title'] = ''
    response = self.post(new_movie)
    self.assertEqual(response.status_code, 400)

    # no genre; fail
    new_movie['genre'] = ''
    response = self.post(new_movie)
    self.assertEqual(response.status_code, 400)

  def test_list(self):
    response = self.client.get('http://localhost:8000/api/movies/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    movies = response.data
    movie_names = [m['title'] for m in movies]

    self.assertIn(self.test_movie['title'], movie_names)

    ids = [m['id'] for m in movies]

    # check if all ids are unique
    self.assertTrue(len(movies) == sum(Counter(ids).values()))

  def test_destroy(self):
    # login and delete as a user; fail
    self.login(self.test_user)
    response = self.delete('1')
    self.assertTrue(response.status_code, 401)

    # log and delete in as a system admin; fail
    self.login(self.test_system_admin)
    response = self.delete('1')
    self.assertTrue(response.status_code, 401)

    # log and delete in as a theater admin; pass
    self.login(self.test_theater_admin)
    response = self.delete('1')
    self.assertTrue(response.status_code, 200)
    self.assertTrue(Movie.objects.all().count() == 0)

    # non-existing movie; fail
    response = self.delete('2')
    self.assertTrue(response.status_code, 404)

  def test_retrieve(self):
    response = self.get('1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(response.data['title'] == self.test_movie['title'])
    self.assertTrue(Movie.objects.get(pk=1).title == self.test_movie['title'])

    # non-existing movie; fail
    response = self.get('2')
    self.assertTrue(response.status_code, 404)

  def test_update(self):
    update_movie = {
      'title': 'title2',
      'genre': 'genre2',
      'director': '',
      'actors': '',
      'duration': '',
      'description': '',
      'theater': 1
    }

    # login and put as a user; fail
    self.login(self.test_user)
    response = self.put(update_movie, '1')
    self.assertEqual(response.status_code, 403)

    # login and put as a system admin; fail
    self.login(self.test_system_admin)
    response = self.put(update_movie, '1')
    self.assertEqual(response.status_code, 403)

    # login and put as a theater admin; pass
    self.login(self.test_theater_admin)
    response = self.put(update_movie, '1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(update_movie['title'] == response.data['title'])
    self.assertTrue(Movie.objects.get(pk=1).title == update_movie['title'])

    # attempt put on a movie that is not theater admins responsibility; fail
    self.login(self.test_theater_admin2)
    response = self.put(update_movie, '1')
    self.assertEqual(response.status_code, 403)

  def test_get_showtimes(self):
    # 0 available showtimes
    response = self.client.get('http://localhost:8000/api/movies/1/showtimes')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 0)

    # showtimes exist
    showtime1 = {
      'auditorium': 'sala1',
      'date': '2018-05-07',
      'time': '15:30',
      'price': 300,
      'movie': 1
    }

    showtime2 = {
      'auditorium': 'sala2',
      'date': '2018-05-07',
      'time': '15:30',
      'price': 300,
      'movie': 1
    }

    serializer = ShowtimeSerializer(data=showtime1)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = ShowtimeSerializer(data=showtime2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    response = self.client.get('http://localhost:8000/api/movies/1/showtimes')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    showtimes = response.data
    ids = [s['id'] for s in showtimes]

    # check if all ids are unique
    self.assertTrue(len(showtimes) == sum(Counter(ids).values()))
