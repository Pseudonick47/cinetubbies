from rest_framework.test import APITestCase

from .models import User
from .serializers import FanZoneAdminSerializer
from .serializers import TheaterAdminSerializer
from .serializers import SystemAdminSerializer

class UserAPI(APITestCase):

  test_user_1 = {
    'username': 'user1',
    'password': '123456',
    'role': 'user',
    'email': 'user@test.com',
  }

  test_user_2 = {
    'username': 'user1',
    'password': '123456',
    'role': 'user',
    'email': 'user@test.com',
  }

  test_user_3 = {
    'username': 'user3',
    'password': '',
    'role': 'user',
    'email': 'user3@test.com',
  }

  def register(self, user):
    response = self.client.post(
      path='http://localhost:8000/api/auth/register/',
      data = {
        'username': user['username'],
        'password': user['password']
      },
      format='json'
    )
    if 'token' in response.data:
      self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])
    return response

  def login(self, user):
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': user['username'],
        'password': user['password']
      },
      format='json'
    )
    if 'token' in response.data:
      self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])
    return response

  def test_user_authentication(self):
    response = self.client.get(path='http://localhost:8000/api/auth/me/')
    self.assertEqual(response.status_code, 401)

    response = self.register(self.test_user_1)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['user']['username'], self.test_user_1['username'])

    response = self.register(self.test_user_2)
    self.assertEqual(response.status_code, 400)

    response = self.register(self.test_user_3)
    self.assertEqual(response.status_code, 400)

    response = self.login(self.test_user_1)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['user']['username'], self.test_user_1['username'])

    response = self.client.get(path='http://localhost:8000/api/auth/me/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['username'], self.test_user_1['username'])

    response = self.login(self.test_user_3)
    self.assertEqual(response.status_code, 400)


class SystemAdminAPI(APITestCase):

  test_fan_zone_admin = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'fan_zone_admin',
    'theater': '',
  }

  test_theater_admin = {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_system_admin = {
    'username': 'sysadmin',
    'password': '123456',
    'role': 'admin',
    'email': 'sysadmin@test.com',
  }

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

  def setUp(self):
    serializer = FanZoneAdminSerializer(data=self.test_fan_zone_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = SystemAdminSerializer(data=self.test_system_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def test_list(self):
    response = self.client.get(path='http://localhost:8000/api/admins/')
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)

    response = self.client.get(path='http://localhost:8000/api/admins/')
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)

    response = self.client.get(path='http://localhost:8000/api/admins/')
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)

    response = self.client.get(path='http://localhost:8000/api/admins/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    response = self.client.get(path='http://localhost:8000/api/admins/?role=fan_zone_admin')
    self.assertEqual(len(response.data), 1)
    self.assertEqual(self.test_fan_zone_admin['username'], response.data[0]['username'])

    response = self.client.get(path='http://localhost:8000/api/admins/?role=cinema_admin')
    self.assertEqual(len(response.data), 1)
    self.assertEqual(self.test_theater_admin['username'], response.data[0]['username'])

    response = self.client.get(path='http://localhost:8000/api/admins/?role=admin')
    self.assertEqual(len(response.data), 1)
    self.assertEqual(self.test_system_admin['username'], response.data[0]['username'])

    test_system_admin2 = {
      'username': 'sysadmin2',
      'password': '123456',
      'role': 'admin',
      'email': 'sysadmin2@test.com',
    }

    serializer = SystemAdminSerializer(data=test_system_admin2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    response = self.client.get(path='http://localhost:8000/api/admins/?role=admin')
    self.assertEqual(len(response.data), 2)
    self.assertIn(
      response.data[0]['username'],
      [self.test_system_admin['username'], test_system_admin2['username']]
    )
    self.assertIn(
      response.data[1]['username'],
      [self.test_system_admin['username'], test_system_admin2['username']]
    )

  def test_create(self):
    test_system_admin2 = {
      'username': 'sysadmin2',
      'role': 'admin',
      'email': 'sysadmin2@test.com',
    }

    response = self.client.post(
      path='http://localhost:8000/api/admins/',
      data=test_system_admin2
    )
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)
    response = self.client.post(
      path='http://localhost:8000/api/admins/',
      data=test_system_admin2,
      format='json'
    )
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)
    response = self.client.post(
      path='http://localhost:8000/api/admins/',
      data=test_system_admin2,
      format='json'
    )
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)
    response = self.client.post(
      path='http://localhost:8000/api/admins/',
      data=test_system_admin2,
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(test_system_admin2['username'], response.data['username'])

    self.assertTrue(User.objects.get(username=test_system_admin2['username']))


  def test_count(self):
    response = self.client.get(path='http://localhost:8000/api/admins/count')
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)

    response = self.client.get(path='http://localhost:8000/api/admins/count')
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)

    response = self.client.get(path='http://localhost:8000/api/admins/count')
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)

    response = self.client.get(path='http://localhost:8000/api/admins/count')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 3)

    test_system_admin2 = {
      'username': 'sysadmin12',
      'password': '123456',
      'role': 'admin',
      'email': 'sysadmin12@test.com',
    }

    serializer = SystemAdminSerializer(data=test_system_admin2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    response = self.client.get(path='http://localhost:8000/api/admins/count')
    self.assertEqual(response.data, 4)

    response = self.client.get(path='http://localhost:8000/api/admins/count?role=admin')
    self.assertEqual(response.data, 2)

    response = self.client.get(path='http://localhost:8000/api/admins/count?role=cinema_admin')
    self.assertEqual(response.data, 1)

    response = self.client.get(path='http://localhost:8000/api/admins/count?role=fan_zone_admin')
    self.assertEqual(response.data, 1)

    User.objects.exclude(role='admin').delete()

    response = self.client.get(path='http://localhost:8000/api/admins/count')
    self.assertEqual(response.data, 2)
