from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

from authentication.serializers import TheaterAdminSerializer
from authentication.serializers import AdminSerializer

from theaters.serializers import AdministrationSerializer as TheaterSerializer

from .categories.models import Category
from .categories.serializers import AdministrationSerializer as \
                                    AdminCategorySerializer

from .props.models import Prop
from .props.official.serializers import RestrictedSerializer as \
                                        RestrictedOfficialPropSerializer
from .props.used.serializers import MemberSerializer as MemberUsedPropSerializer


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

  test_fan_zone_admin = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'fan_zone_admin',
  }

  test_theater = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'admins': [1],
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
    'categoryId': 1,
    'quantity': 2,
    'price': 99.9,
    'theaterId': 1,
    'imageId': None,
    'kind': 'O'
  }

  test_prop_2 = {
    'title': 'Prop2',
    'description': 'some profound text here',
    'categoryId': 2,
    'quantity': 5,
    'price': 59.9,
    'theaterId': 1,
    'imageId': None,
    'kind': 'O'
  }

  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_fan_zone_admin)
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
    self.assertEqual(response.status_code, 404)


    Prop.official.all().delete()

    response = self.client.get(path='http://localhost:8000/api/props/official/')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.data)

  def test_count(self):
    response = self.client.get(path='http://localhost:8000/api/props/official/count')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 2)

    response = self.client.get(path='http://localhost:8000/api/props/categories/1/official/count')
    self.assertEqual(response.status_code, 404)

    Prop.official.all().delete()

    response = self.client.get(path='http://localhost:8000/api/props/official/count')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.data)

class RestrictedOfficialPropAPITests(APITestCase):

  test_theater_admin = {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_fan_zone_admin = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'fan_zone_admin',
  }

  test_fan_zone_admin_2 = {
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

  test_theater = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'theater': [1],
    'admins': [1]
  }

  test_theater_2 = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'admins': [1],
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
    'categoryId': 1,
    'quantity': 2,
    'price': 99.9,
    'theaterId': 1,
    'imageId': None,
    'kind': 'O'
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
      path='http://localhost:8000/api/props/official/',
      data=data,
      format='json'
    )

  def delete(self, id):
    return self.client.delete(
      path="http://localhost:8000/api/props/official/" + str(id)
    )

  def put(self, id, data):
    return self.client.put(
      path="http://localhost:8000/api/props/official/" + str(id),
      data=data,
      format='json'
    )

  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_fan_zone_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_fan_zone_admin_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_system_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterSerializer(data=self.test_theater)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterSerializer(data=self.test_theater_2)
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

  def test_create(self):
    test_prop_2 = {
      'title': 'Prop2',
      'description': 'some profound text here',
      'categoryId': 2,
      'quantity': 5,
      'price': 59.9,
      'theaterId': 1,
      'imageId': None,
      'kind': 'O'
    }

    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_theater_admin)
    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_fan_zone_admin)
    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    self.login(self.test_system_admin)
    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 200)

  def test_destroy(self):
    test_prop_2 = {
      'title': 'Prop2',
      'description': 'some profound text here',
      'categoryId': 2,
      'quantity': 5,
      'price': 59.9,
      'theaterId': 2,
      'imageId': None,
      'kind': 'O'
    }

    serializer = RestrictedOfficialPropSerializer(data=test_prop_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    response = self.delete(2)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_theater_admin)
    response = self.delete(2)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_fan_zone_admin_2)
    response = self.delete(2)
    self.assertEqual(response.status_code, 200)

    serializer = RestrictedOfficialPropSerializer(data=test_prop_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = RestrictedOfficialPropSerializer(data=test_prop_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    self.login(self.test_system_admin)
    response = self.delete(3)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    self.login(self.test_system_admin)
    response = self.delete(1)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    response = self.delete(99)
    self.assertEqual(response.status_code, 404)

  def test_update(self):
    test_prop_2 = {
      'title': 'Prop2',
      'description': 'some profound text here',
      'categoryId': 2,
      'quantity': 5,
      'price': 59.9,
      'theaterId': 1,
      'imageId': None,
      'kind': 'O'
    }

    serializer = RestrictedOfficialPropSerializer(data=test_prop_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    response = self.put(2, test_prop_2)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_theater_admin)
    response = self.put(2, test_prop_2)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_fan_zone_admin)
    response = self.put(2, test_prop_2)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)


class PublicUsedAPI(APITestCase):

  test_user = {
    'username': 'user',
    'password': '123456',
    'email': 'user@test.com',
    'role': 'user',
  }

  test_theater_admin = {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_fan_zone_admin = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'fan_zone_admin',
  }

  test_theater = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'admins': [1],
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
    'ownerId': 1,
    'categoryId': 1,
    'imageId': None,
    'expirationDate': '2018-06-01',
    'kind': 'U'
  }

  test_prop_2 = {
    'title': 'Prop2',
    'description': 'some profound text here',
    'ownerId': 1,
    'categoryId': 2,
    'imageId': None,
    'expirationDate': '2018-06-06',
    'kind': 'U'
  }

  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminSerializer(data=self.test_fan_zone_admin)
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

    serializer = MemberUsedPropSerializer(data=self.test_prop_1)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = MemberUsedPropSerializer(data=self.test_prop_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def test_list(self):
    response = self.client.get(path='http://localhost:8000/api/props/used/?all=true')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 2)

    response = self.client.get(path='http://localhost:8000/api/props/used/?category=1&all=true')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 1)

    response = self.client.get(path='http://localhost:8000/api/props/used/?category=2&all=true')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(len(response.data), 1)

    response = self.client.get(path='http://localhost:8000/api/props/used/?category=99&all=true')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 0)

    Prop.used.all().delete()

    response = self.client.get(path='http://localhost:8000/api/props/used/?all=true')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.data)

  def test_count(self):
    response = self.client.get(path='http://localhost:8000/api/props/used/count?all=true')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 2)

    response = self.client.get(path='http://localhost:8000/api/props/used/count?category=1&all=true')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 1)

    response = self.client.get(path='http://localhost:8000/api/props/used/count?category=1&all=true')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 1)

    response = self.client.get(path='http://localhost:8000/api/props/used/count?category=99&all=true')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, 0)

    Prop.used.all().delete()

    response = self.client.get(path='http://localhost:8000/api/props/used/count?all=true')
    self.assertEqual(response.status_code, 200)
    self.assertFalse(response.data)


class MemberUsedPropAPITests(APITestCase):

  test_user = {
    'username': 'user',
    'password': '123456',
    'email': 'user@test.com',
    'role': 'user',
  }

  test_theater_admin = {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_fan_zone_admin = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'fan_zone_admin',
  }

  test_system_admin = {
    'username': 'sysadmin',
    'password': '123456',
    'role': 'admin',
    'email': 'sysadmin@test.com',
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
    'ownerId': 1,
    'categoryId': 1,
    'imageId': None,
    'expirationDate': '2018-06-01',
    'kind': 'U'
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
      path='http://localhost:8000/api/props/used/',
      data=data,
      format='json'
    )

  def delete(self, id):
    return self.client.delete(
      path="http://localhost:8000/api/props/used/" + str(id)
    )

  def put(self, id, data):
    return self.client.put(
      path="http://localhost:8000/api/props/used/" + str(id),
      data=data,
      format='json'
    )

  def setUp(self):
    serializer = AdminSerializer(data=self.test_user)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
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

    serializer = AdminCategorySerializer(data=self.test_category_1)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminCategorySerializer(data=self.test_category_2)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = MemberUsedPropSerializer(data=self.test_prop_1)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def test_create(self):
    test_prop_2 = {
      'title': 'Prop2',
      'description': 'some profound text here',
      'ownerId': 1,
      'categoryId': 2,
      'imageId': None,
      'expirationDate': '2018-06-01',
      'kind': 'U'
    }

    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_user)
    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 200)

    self.login(self.test_theater_admin)
    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 200)

    self.login(self.test_fan_zone_admin)
    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    self.login(self.test_system_admin)
    response = self.post(test_prop_2)
    self.assertEqual(response.status_code, 200)

  # def test_destroy(self):
  #   test_prop_2 = {
  #     'title': 'Prop2',
  #     'description': 'some profound text here',
  #     'ownerId': 1,
  #     'categoryId': 2,
  #     'imageId': None,
  #     'expirationDate': '2018-06-01',
      # 'kind': 'U'
  #   }

  #   serializer = MemberUsedPropSerializer(data=test_prop_2)
  #   if not serializer.is_valid():
  #     raise Exception(serializer.errors)
  #   serializer.save()

  #   response = self.delete(2)
  #   self.assertEqual(response.status_code, 401)

  #   self.login(self.test_user)
  #   response = self.delete(2)
  #   self.assertEqual(response.status_code, 200)

  #   self.login(self.test_theater_admin)
  #   response = self.delete(2)
  #   self.assertEqual(response.status_code, 403)

  #   self.login(self.test_fan_zone_admin)
  #   response = self.delete(2)
  #   self.assertEqual(response.status_code, 403)

  #   self.login(self.test_user)
  #   response = self.delete(2)
  #   self.assertEqual(response.status_code, 200)

  #   serializer = MemberUsedPropSerializer(data=test_prop_2)
  #   if not serializer.is_valid():
  #     raise Exception(serializer.errors)
  #   serializer.save()

  #   serializer = MemberUsedPropSerializer(data=test_prop_2)
  #   if not serializer.is_valid():
  #     raise Exception(serializer.errors)
  #   serializer.save()

  #   self.login(self.test_system_admin)
  #   response = self.delete(3)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertTrue(response.data)

  #   self.login(self.test_system_admin)
  #   response = self.delete(1)
  #   self.assertEqual(response.status_code, 200)
  #   self.assertTrue(response.data)

  #   response = self.delete(99)
  #   self.assertEqual(response.status_code, 404)

  # def test_update(self):
  #   test_prop_2 = {
  #     'title': 'Prop2',
  #     'description': 'some profound text here',
  #     'ownerId': 1,
  #     'categoryId': 2,
  #     'imageId': None,
  #     'expirationDate': '2018-06-01',
    #   'kind': 'U'
  #   }

  #   serializer = MemberUsedPropSerializer(data=test_prop_2)
  #   if not serializer.is_valid():
  #     raise Exception(serializer.errors)
  #   serializer.save()

  #   response = self.put(2, test_prop_2)
  #   self.assertEqual(response.status_code, 401)

  #   self.login(self.test_theater_admin)
  #   response = self.put(2, test_prop_2)
  #   self.assertEqual(response.status_code, 403)

  #   self.login(self.test_fan_zone_admin)
  #   response = self.put(2, test_prop_2)
  #   self.assertEqual(response.status_code, 403)

  #   self.login(self.test_user)
  #   response = self.put(2, test_prop_2)
  #   self.assertEqual(response.status_code, 200)

class RestrictedUsedPropAPITests(APITestCase):

  test_user = {
    'username': 'user',
    'password': '123456',
    'email': 'user@test.com',
    'role': 'user',
  }

  test_theater_admin = {
    'username': 'admin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'cinema_admin',
    'theater': '',
  }

  test_fan_zone_admin = {
    'username': 'admin2',
    'password': '123456',
    'email': 'admin2@test.com',
    'role': 'fan_zone_admin',
  }

  test_system_admin = {
    'username': 'sysadmin',
    'password': '123456',
    'role': 'admin',
    'email': 'sysadmin@test.com',
  }

  test_theater = {
    'name': 'theater1',
    'address': 'some street',
    'kind': 'p',
    'admins': [2],
  }

  test_category = {
    'name': 'cat',
    'supercategory': None
  }

  test_prop = {
    'title': 'Prop1',
    'description': 'some profound text here',
    'ownerId': 1,
    'categoryId': 1,
    'imageId': None,
    'expirationDate': '2018-06-01',
    'kind': 'U'
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


  def put(self, id, data):
    return self.client.put(
      path="http://localhost:8000/api/props/used/" + str(id) + "/review",
      data=data,
      format='json'
    )

  def setUp(self):
    serializer = AdminSerializer(data=self.test_user)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
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

    serializer = TheaterSerializer(data=self.test_theater)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = AdminCategorySerializer(data=self.test_category)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

    serializer = MemberUsedPropSerializer(data=self.test_prop)
    if not serializer.is_valid():
      raise Exception(serializer.errors)
    serializer.save()

  def test_update(self):
    data = {
      'approve': True
    }

    response = self.put(1, data)
    self.assertEqual(response.status_code, 401)

    self.login(self.test_user)
    response = self.put(1, data)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_theater_admin)
    response = self.put(1, data)
    self.assertEqual(response.status_code, 403)

    self.login(self.test_fan_zone_admin)
    response = self.put(1, data)
    self.assertEqual(response.status_code, 200)

    self.login(self.test_system_admin)
    response = self.put(1, data)
    self.assertEqual(response.status_code, 200)
