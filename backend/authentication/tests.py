from rest_framework.test import APITestCase

from .models import User
from .serializers import TheaterAdminSerializer
from .serializers import AdminSerializer

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


class FriendAPI(APITestCase):
  test_user_1 = {
    'username': 'user11',
    'first_name': 'arst',
    'password': '123456',
    'phone': '12312',
    'city': 'NS',
    'role': 'user',
    'email': 'user@test.com',
  }

  test_user_2 = {
    'username': 'user22',
    'first_name': 'user',
    'password': '123456',
    'phone': '12312',
    'city': 'NS',
    'role': 'user',
    'email': 'user2@test.com',
  }

  test_user_3 = {
    'username': 'user33',
    'first_name': 'userrr',
    'password': '123456',
    'phone': '12312',
    'city': 'NS',
    'role': 'user',
    'email': 'user3@test.com',
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
    if 'token' in response.data:
      self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])
    return response

  def setUp(self):
    serializer = AdminSerializer(data=self.test_user_1)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_user_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_user_3)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def test_friends(self):
    self.login(self.test_user_1)

    response = self.client.get(path='http://localhost:8000/api/users/1/friends/')
    self.assertEqual(response.data['friends'], [])
    self.assertEqual(response.data['friend_requests'], [])

    response = self.client.get(path='http://localhost:8000/api/users/friends/use')
    self.assertEqual(len(response.data['results']), 2)

    response = self.client.post(path='http://localhost:8000/api/users/2/friends/')
    self.assertEqual(response.status_code, 200)

    self.login(self.test_user_2)

    response = self.client.get(path='http://localhost:8000/api/users/2/friends/')
    self.assertEqual(response.data['friends'], [])
    self.assertEqual(len(response.data['friend_requests']), 1)

    response = self.client.post(path='http://localhost:8000/api/users/1/friends/')
    self.assertEqual(response.status_code, 200)

    self.login(self.test_user_1)

    response = self.client.get(path='http://localhost:8000/api/users/1/friends/')
    self.assertEqual(len(response.data['friends']), 1)
    self.assertEqual(response.data['friend_requests'], [])


class SystemAdminAPI(APITestCase):

  test_fan_zone_admin = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'fan_zone_admin',
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

  test_theater_admin2 = {
    'username': 'admin3',
    'password': '123456',
    'email': 'admin3@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  def patch(self, user, id):
    return self.client.patch(
      path='http://localhost:8000/api/users/'+id+'/',
      data = user,
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

  def setUp(self):
    serializer = AdminSerializer(data=self.test_fan_zone_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_system_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def test_partial_update(self):
    update_user = {
      'name': 'name'
    }

    # user changes the profile info of another user; fail
    self.login(self.test_theater_admin2)
    response = self.patch(update_user,'2')
    self.assertEqual(response.status_code, 403)

    # user changes his profile info; pass
    self.login(self.test_theater_admin)
    response = self.patch(update_user,'2')
    self.assertEqual(response.status_code, 200)

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
    self.assertEqual(len(response.data), 2)
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

    serializer = AdminSerializer(data=test_system_admin2)
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
      data=test_system_admin2,
      format='json'
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
    self.assertEqual(response.data, 4)

    test_system_admin2 = {
      'username': 'sysadmin12',
      'password': '123456',
      'role': 'admin',
      'email': 'sysadmin12@test.com',
    }

    serializer = AdminSerializer(data=test_system_admin2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    response = self.client.get(path='http://localhost:8000/api/admins/count')
    self.assertEqual(response.data, 5)

    response = self.client.get(path='http://localhost:8000/api/admins/count?role=admin')
    self.assertEqual(response.data, 2)

    response = self.client.get(path='http://localhost:8000/api/admins/count?role=cinema_admin')
    self.assertEqual(response.data, 2)

    response = self.client.get(path='http://localhost:8000/api/admins/count?role=fan_zone_admin')
    self.assertEqual(response.data, 1)

    User.objects.exclude(role='admin').delete()

    response = self.client.get(path='http://localhost:8000/api/admins/count')
    self.assertEqual(response.data, 2)
