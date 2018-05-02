from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

from authentication.serializers import FanZoneAdminSerializer
from authentication.serializers import TheaterAdminSerializer
from authentication.serializers import SystemAdminSerializer

from theaters.serializers import AdministrationSerializer as TheaterSerializer

from .models import Category
from .models import OfficialProp
from .serializers import AdminCategorySerializer
from .serializers import RestrictedOfficialPropSerializer

class PublicCategoryAPI(APITestCase):

  test_category = {
    'name': 'cat',
    'supercategory': None
  }

  test_subcategory = {
    'name': 'cat',
    'supercategory': 1
  }

  def setUp(self):
    serializer = AdminCategorySerializer(data=self.test_category)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminCategorySerializer(data=self.test_subcategory)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def test_list(self):
    response = self.client.get('http://localhost:8000/api/props/categories/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 2)

    Category.objects.all().delete()
    response = self.client.get('http://localhost:8000/api/props/categories/')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.data)

  def test_retrieve(self):
    response = self.client.get('http://localhost:8000/api/props/categories/1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(self.test_category['name'], response.data['name'])

    response = self.client.get('http://localhost:8000/api/props/categories/2')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(self.test_subcategory['name'], response.data['name'])

    response = self.client.get('http://localhost:8000/api/props/categories/99')
    self.assertEqual(response.status_code, 404)


class AdminCategoryAPI(APITestCase):

  test_category = {
    'name': 'cat',
    'supercategory': None
  }

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

  def post(self, data):
    return self.client.post(
      path='http://localhost:8000/api/props/categories/',
      data=data,
      format='json'
    )

  def delete(self, id):
    return self.client.delete(
      path="http://localhost:8000/api/props/categories/" + str(id)
    )

  def put(self, id, data):
    return self.client.delete(
      path="http://localhost:8000/api/props/categories/" + str(id),
      data=data,
      format='json'
    )

  def setUp(self):
    serializer = AdminCategorySerializer(data=self.test_category)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

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

  def test_create(self):
    subcategory = {
      'name': 'cat',
      'supercategory': 1
    }

    response = self.post(subcategory)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)
    response = self.post(subcategory)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)
    response = self.post(subcategory)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)
    response = self.post(subcategory)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    subcategory = {
      'supercategory': 1
    }
    response = self.post(subcategory)
    self.assertEqual(response.status_code, 400)

    subcategory = {
      'name': 'cat',
    }
    response = self.post(subcategory)
    self.assertEqual(response.status_code, 400)

    subcategory = {
    }
    response = self.post(subcategory)
    self.assertEqual(response.status_code, 400)


  def test_destroy(self):
    response = self.delete(1)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)
    response = self.delete(1)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)
    response = self.delete(1)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)
    response = self.delete(1)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    response = self.delete(99)
    self.assertEqual(response.status_code, 404)

  def test_update(self):
    category = {
      'name': 'cat2',
      'supercategory': None
    }

    response = self.put(1, category)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_fan_zone_admin)
    response = self.put(1, category)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)
    response = self.put(1, category)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_system_admin)
    response = self.put(1, category)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)


class PublicOfficialPropAPI(APITestCase):
  test_theater_admin = {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_theater = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'theateradmins': [1],
  }

  test_category_1 = {
    'name': 'cat',
    'supercategory': None
  }

  test_category_2 = {
    'name': 'cat2',
    'supercategory': None
  }

  test_prop_1 = {
    'title': 'Prop1',
    'description': 'some profound text here',
    'category': 1,
    'quantity': 2,
    'price': 99.9,
    'theater': 1,
    'image_id': None
  }

  test_prop_2 = {
    'title': 'Prop2',
    'description': 'some profound text here',
    'category': 2,
    'quantity': 5,
    'price': 59.9,
    'theater': 1,
    'image_id': None
  }

  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterSerializer(data=self.test_theater)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminCategorySerializer(data=self.test_category_1)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminCategorySerializer(data=self.test_category_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = RestrictedOfficialPropSerializer(data=self.test_prop_1)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = RestrictedOfficialPropSerializer(data=self.test_prop_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def test_list(self):
    response = self.client.get(path='http://localhost:8000/api/props/official/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 2)

    response = self.client.get(path='http://localhost:8000/api/props/categories/1/official/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 1)

    response = self.client.get(path='http://localhost:8000/api/props/categories/2/official/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 1)

    response = self.client.get(path='http://localhost:8000/api/props/categories/99/official/')
    self.assertEqual(response.status_code, 404)

    response = self.client.get(path='http://localhost:8000/api/theaters/1/props/official/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 2)

    response = self.client.get(path='http://localhost:8000/api/theaters/99/props/official/')
    self.assertEqual(response.status_code, 404)

    response = self.client.get(path='http://localhost:8000/api/theaters/1/props/categories/1/official/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 1)

    OfficialProp.objects.all().delete()

    response = self.client.get(path='http://localhost:8000/api/props/official/')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.data)

  def test_count(self):
    response = self.client.get(path='http://localhost:8000/api/props/official/count')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 2)

    response = self.client.get(path='http://localhost:8000/api/props/categories/1/official/count')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 1)

    response = self.client.get(path='http://localhost:8000/api/props/categories/2/official/count')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 1)

    response = self.client.get(path='http://localhost:8000/api/props/categories/99/official/count')
    self.assertEqual(response.status_code, 404)

    response = self.client.get(path='http://localhost:8000/api/theaters/1/props/official/count')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 2)

    response = self.client.get(path='http://localhost:8000/api/theaters/99/props/official/count')
    self.assertEqual(response.status_code, 404)

    response = self.client.get(path='http://localhost:8000/api/theaters/1/props/categories/1/official/count')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 1)

    OfficialProp.objects.all().delete()

    response = self.client.get(path='http://localhost:8000/api/props/official/count')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.data)
