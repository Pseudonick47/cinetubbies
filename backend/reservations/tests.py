from rest_framework.test import APITestCase

from authentication.serializers import AdminSerializer
from authentication.serializers import TheaterAdminSerializer

class RewardScaleAPITests(APITestCase):

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

  def test_list(self):
    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/')
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/')
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/')
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

  def test_retrieve(self):
    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/basic')
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/basic')
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/basic')
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/basic')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/bronze')
    self.assertEqual(response.status_code, 200)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/silver')
    self.assertEqual(response.status_code, 200)

    response = self.client.get(path='http://localhost:8000/api/reservations/rewards/gold')
    self.assertEqual(response.status_code, 200)

  def test_update(self):
    scale = {
      'status': 'basic',
      'min': 10,
      'max': 25
    }

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/basic',
      data=scale,
      format='json'
    )
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/basic',
      data=scale,
      format='json'
    )
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/basic',
      data=scale,
      format='json'
    )
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/basic',
      data=scale,
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    scale = {
      'status': 'bronze',
      'min': 10,
      'max': 25
    }

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/bronze',
      data=scale,
      format='json'
    )
    self.assertEqual(response.status_code, 200)

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/silver',
      data=scale,
      format='json'
    )
    self.assertEqual(response.status_code, 200)

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/gold',
      data=scale,
      format='json'
    )
    self.assertEqual(response.status_code, 200)

  def test_update_all(self):
    scales = [
      {
        'status': 'basic',
        'min': 10,
        'max': 25
      },
      {
        'status': 'bronze',
        'min': 10,
        'max': 25
      },
      {
        'status': 'silver',
        'min': 10,
        'max': 25
      },
      {
        'status': 'gold',
        'min': 10,
        'max': 25
      }
    ]

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/',
      data=scales,
      format='json'
    )
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/',
      data=scales,
      format='json'
    )
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/',
      data=scales,
      format='json'
    )
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)

    response = self.client.put(
      path='http://localhost:8000/api/reservations/rewards/',
      data=scales,
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
