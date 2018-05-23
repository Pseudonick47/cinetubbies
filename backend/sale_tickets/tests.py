from rest_framework.test import APITestCase

from authentication.models import User
# from authentication.serializers import FanZoneAdminSerializer
# from authentication.serializers import SystemAdminSerializer
from authentication.serializers import AdminSerializer
from authentication.serializers import TheaterAdminSerializer
from authentication.serializers import UserSerializer

from theaters.models import Theater
from theaters.serializers import AdministrationSerializer
from theaters.serializers import PublicSerializer
from theaters.serializers import AuditoriumSerializer

from movies.models import Movie
from movies.serializers import MovieSerializer

from showtimes.models import Showtime
from showtimes.serializers import ShowtimeSerializer

from .models import TicketOnSale
from .serializers import TicketOnSaleSerializer

class TicketOnSaleAPITests(APITestCase):
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
    'theater': '',
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
    'admins': [2]
  }

  auditorium = {
    'name': 'Sala 1',
    'theater': 1,
    'layout': '{}'
  }

  test_movie = {
    'title': 'title',
    'genre': 'genre',
    'theater': 1
  }

  test_showtime = {
      'auditorium': 1,
      'date': '2018-05-10',
      'time': '15:00',
      'price': 300,
      'movie': 1
    }

  test_ticket = {
      'seat': 1,
      'discount': 20,
      'showtime': 1,
      'theater': 1
    }

  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin2)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_fan_zone_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_system_admin)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = UserSerializer(data=self.test_user)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = AdministrationSerializer(data=self.test_theater)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = AdministrationSerializer(data=self.test_theater2)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = AuditoriumSerializer(data=self.auditorium)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = MovieSerializer(data=self.test_movie)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = ShowtimeSerializer(data=self.test_showtime)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = TicketOnSaleSerializer(data=self.test_ticket)
    if not serializer.is_valid():
      print(serializer.errors)
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

  def post(self, new_ticket):
    return self.client.post(
      path='http://localhost:8000/api/sale/',
      data = new_ticket,
      format='json'
    )

  def delete(self, id):
    return self.client.delete(
      path='http://localhost:8000/api/sale/'+id+'/'
    )

  def get(self, id):
    return self.client.get(
      path='http://localhost:8000/api/sale/'+id+'/'
    )

  def put(self, ticket, id):
    return self.client.put(
      path='http://localhost:8000/api/sale/'+id+'/',
      data = ticket,
      format='json'
    )

  def test_create(self):
    new_ticket = {
      'seat': 2,
      'discount': 20,
      'showtime': 1,
      'theater': 1
    }

    # login and post as a user; fail
    self.login(self.test_user)
    response = self.post(new_ticket)
    self.assertEqual(response.status_code, 403)

    # login and post as a system admin; fail
    self.login(self.test_system_admin)
    response = self.post(new_ticket)
    self.assertEqual(response.status_code, 403)

    # login and post as a theater admin; pass
    self.login(self.test_theater_admin)
    response = self.post(new_ticket)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(TicketOnSale.objects.all().count() == 2)

    # non-existing showtime; fail
    new_ticket['showtime'] = 2
    response = self.post(new_ticket)
    self.assertEqual(response.status_code, 400)

    # non-existing theater; fail
    new_ticket['theater'] = 5
    response = self.post(new_ticket)
    self.assertEqual(response.status_code, 400)

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
    self.assertTrue(TicketOnSale.objects.all().count() == 0)

    # non-existing ticket; fail
    response = self.delete('2')
    self.assertTrue(response.status_code, 404)

  def test_retrieve(self):
    response = self.get('1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    # non-existing ticket; fail
    response = self.get('2')
    self.assertTrue(response.status_code, 404)

  def test_update(self):
    update_ticket = {
      'seat': 3,
      'discount': 30,
      'showtime': 1,
      'theater': 1
    }

    # login and put as a user; fail
    self.login(self.test_user)
    response = self.put(update_ticket, '1')
    self.assertEqual(response.status_code, 403)

    # login and put as a system admin; fail
    self.login(self.test_system_admin)
    response = self.put(update_ticket, '1')
    self.assertEqual(response.status_code, 403)

    # login and put as a theater admin; pass
    self.login(self.test_theater_admin)
    response = self.put(update_ticket, '1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    # attempt put on a ticket that is not theater admin's responsibility; fail
    self.login(self.test_theater_admin2)
    response = self.put(update_ticket, '1')
    self.assertEqual(response.status_code, 403)




class BookingAPITests(APITestCase):

  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_fan_zone_admin)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = UserSerializer(data=self.test_user)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = UserSerializer(data=self.test_user2)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = AdministrationSerializer(data=self.test_theater)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = AuditoriumSerializer(data=self.auditorium)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = MovieSerializer(data=self.test_movie)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = ShowtimeSerializer(data=self.test_showtime)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

  test_theater_admin = {
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
    'theater': '',
  }

  test_user = {
    'username': 'username',
    'password': '123456',
    'phone': '123',
    'city': 'city'
  }

  test_user2 = {
    'username': 'username2',
    'password': '123456',
    'phone': '123',
    'city': 'city'
  }

  test_movie = {
    'title': 'title',
    'genre': 'genre',
    'theater': 1
  }

  test_showtime = {
    'auditorium': 1,
    'date': '2018-05-10',
    'time': '15:00',
    'price': 300,
    'movie': 1
  }

  auditorium = {
    'name': 'Sala 1',
    'theater': 1,
    'layout': '{}'
  }

  test_theater = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'admins': [1]
  }

  valid_data = [
    {
      'showtime': 1,
      'chosen_seats': [1, 3, 4]
    },
    {
      'showtime': 1,
      'chosen_seats': [2, 1]
    },
    {
      'showtime': 1,
      'chosen_seats': [1]
    },
  ]

  invalid_data = [
    {
      'showtime': '',
      'chosen_seats': [1, 3, 4]
    },
    {
      'showtime': 'arst',
      'chosen_seats': [2, 1]
    },
    {
    },
    {
      'chosen_seats': []
    },
  ]

  def book_create(self, booking_data):
    return self.client.post(
      path='http://localhost:8000/api/sale/booking/',
      data = booking_data,
      format='json'
    )

  def book_delete(self, id):
    return self.client.delete(
      path=f'http://localhost:8000/api/sale/booking/{id}/',
      format='json'
    )

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

  def test_create(self):
    response = self.book_create(self.valid_data[0])
    self.assertEqual(response.status_code, 401)

    self.login(self.test_user)
    for test_case_data in self.valid_data:
      response = self.book_create(test_case_data)
      self.assertEqual(response.status_code, 200)
      for key in ['id', 'showtime', 'user', 'discount', 'price', 'seat']:
        self.assertIn(key, response.data)

    for test_case_data in self.invalid_data:
      response = self.book_create(test_case_data)
      self.assertEqual(response.status_code, 400)

  def test_delete(self):
    self.login(self.test_user)
    for test_case_data in self.valid_data:
      response = self.book_create(test_case_data)

    self.client.credentials(HTTP_AUTHORIZATION='')

    response = self.book_delete(1)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_user)

    response = self.book_delete(1)
    self.assertEqual(response.status_code, 200)

    response = self.book_delete(1)
    self.assertEqual(response.status_code, 404)

    self.client.credentials(HTTP_AUTHORIZATION='')
    self.login(self.test_user2)

    response = self.book_delete(2)
    self.assertEqual(response.status_code, 403)
