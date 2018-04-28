from collections import Counter
from copy import deepcopy
from rest_framework.test import APITestCase

from authentication.models import User
from authentication.serializers import AdminSerializer
from authentication.serializers import TheaterAdminSerializer

from .models import Theater
from .serializers import AdministrationSerializer
from .serializers import PublicSerializer


class TheaterAPITests(APITestCase):
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
    'admins': [1],
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

    serializer = AdminSerializer(data=self.test_system_admin)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = AdministrationSerializer(data=self.test_theater)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

  def test_create(self):
    new_theater = {
      'name': 'theater2',
      'address': 'some street',
      'kind': 'm',
      'admins': [1],
    }

    # attempt post as a user; should fail
    response = self.client.post(
      path='http://localhost:8000/api/theaters/',
      data = new_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 401)

    # login as a theater admin
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_theater_admin['username'],
        'password': self.test_theater_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    # attempt post as a theater admin; should fail
    response = self.client.post(
      path='http://localhost:8000/api/theaters/',
      data = new_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 403)

    # login as a system admin
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_system_admin['username'],
        'password': self.test_system_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    # attempt post as a system admin; should pass
    response = self.client.post(
      path='http://localhost:8000/api/theaters/',
      data = new_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(Theater.objects.all().count() == 2)

    new_theater['kind'] = 's'

    # attempt creating a theater with an invalid kind value
    response = self.client.post(
      path='http://localhost:8000/api/theaters/',
      data = new_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 400)

    new_theater['admins'] = [99]

    # attempt create a theater with a non-existing admin
    response = self.client.post(
      path='http://localhost:8000/api/theaters/',
      data = new_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 400)

    # cleanup
    Theater.objects.get(pk=2).delete()

  def test_list(self):
    response = self.client.get('http://localhost:8000/api/theaters/')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

    theaters = response.data
    theater_names = [t['name'] for t in theaters]

    self.assertIn(self.test_theater['name'], theater_names)

    ids = [t['id'] for t in theaters]
    # check if all ids are unique
    self.assertTrue(len(theaters) == sum(Counter(ids).values()))

  def test_retrieve(self):
    response = self.client.get('http://localhost:8000/api/theaters/1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(response.data['name'] == self.test_theater['name'])
    self.assertTrue(Theater.objects.get(pk=1).name == self.test_theater['name'])

    # request a non-existing theater; should fail
    response = self.client.get('http://localhost:8000/api/theaters/99')
    self.assertTrue(response.status_code, 404)

  def test_update(self):
    new_theater = {
      'name': 'theater1',
      'address': 'some street',
      'kind': 'p',
      'admins': [1],
    }

    serializer = AdministrationSerializer(data=new_theater)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    update_theater = {
      'name': 'theater2',
      'address': 'some street',
      'kind': 'm',
    }

    # attempt put as a user; should fail
    response = self.client.put(
      path='http://localhost:8000/api/theaters/2',
      data = update_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 401)

    # log in as a theater admin
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_theater_admin['username'],
        'password': self.test_theater_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    # attempt put as a theater admin; should pass
    response = self.client.put(
      path='http://localhost:8000/api/theaters/2',
      data = update_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(update_theater['name'] == response.data['name'])
    self.assertTrue(Theater.objects.get(pk=2).name == update_theater['name'])

    # attempt put on a theater that is not theater admins responsibility;
    # should fail
    response = self.client.put(
      path='http://localhost:8000/api/theaters/1',
      data = update_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 403)

    # check for all other theater fields
    update_theater = {
      'name': 'theater2',
      'address': 'some street2',
      'kind': 'p',
    }

    response = self.client.put(
      path='http://localhost:8000/api/theaters/2',
      data = update_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(update_theater['address'] == response.data['address'])
    self.assertTrue(
      Theater.objects.get(pk=2).address == update_theater['address']
    )
    self.assertTrue(
      Theater.objects.get(pk=2).kind == update_theater['kind']
    )

    update_theater['kind'] = 's'
    # attempt updating theater kind to a invalid value; should fail
    response = self.client.put(
      path='http://localhost:8000/api/theaters/2',
      data = update_theater,
      format='json'
    )
    self.assertTrue(response.status_code, 404)
    # check that fail happend before db update or db has a constraint to prevent
    # this situation
    self.assertTrue(Theater.objects.get(pk=1).kind != update_theater['kind'])

     # log in as a system admin
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_system_admin['username'],
        'password': self.test_system_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    update_theater['name'] = 'some new name'
    update_theater['kind'] = 'p'

    # attempt put as a system admin; should pass
    response = self.client.put(
      path='http://localhost:8000/api/theaters/2',
      data = update_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(update_theater['name'] == response.data['name'])

    update_theater['name'] = 'some new name'

    # attempt put as a system admin on a different theater; should pass
    response = self.client.put(
      path='http://localhost:8000/api/theaters/1',
      data = update_theater,
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(update_theater['name'] == response.data['name'])


  def test_update_admin(self):
    # attempt put as a user; should fail
    response = self.client.put(
      path='http://localhost:8000/api/theaters/1/admins/',
      data = { 'admins': [2] },
      format='json'
    )
    self.assertTrue(response.status_code, 401)

    # log in as a theater admin
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_theater_admin['username'],
        'password': self.test_theater_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    # attempt put as a theater admin; should fail
    response = self.client.put(
      path='http://localhost:8000/api/theaters/1/admins/',
      data = { 'admins': [2] },
      format='json'
    )
    self.assertTrue(response.status_code, 401)

    # log in as a system admin
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_system_admin['username'],
        'password': self.test_system_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    # attempt put as a system admin; should pass
    response = self.client.put(
      path='http://localhost:8000/api/theaters/1/admins/',
      data = { 'admins': [2] },
      format='json'
    )
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertTrue(response.data['admins'] == [2])
    self.assertTrue(list(Theater.objects.get(pk=1).admins.all())[0].id == 2)

    # set theater admin to a non-existing user; should fail
    response = self.client.put(
      path='http://localhost:8000/api/theaters/1/admins/',
      data = { 'admins': [99] },
      format='json'
    )
    self.assertTrue(response.status_code, 400)

  def test_destroy(self):
    # attempt delete as a user; should fail
    response = self.client.delete(
      path='http://localhost:8000/api/theaters/1'
    )
    self.assertTrue(response.status_code, 401)

    # log in as a theater admin
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_theater_admin['username'],
        'password': self.test_theater_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    # attempt delete as a theater admin; should fail
    response = self.client.delete(
      path='http://localhost:8000/api/theaters/1'
    )
    self.assertTrue(response.status_code, 401)

    # log in as a system admin
    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_system_admin['username'],
        'password': self.test_system_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    # attempt delete as a system admin; should pass
    response = self.client.delete(
      path='http://localhost:8000/api/theaters/1'
    )
    self.assertTrue(response.status_code, 200)

    # try to delete a non-existing theater; should fail
    response = self.client.delete(
      path='http://localhost:8000/api/theaters/999'
    )
    self.assertTrue(response.status_code, 404)


  def test_count(self):
    response = self.client.get('http://localhost:8000/api/theaters/count')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)
    self.assertEqual(response.data, 1)

    new_theater = deepcopy(self.test_theater)
    serializer = AdministrationSerializer(data=new_theater)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    response = self.client.get('http://localhost:8000/api/theaters/count')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, 2)

    Theater.objects.get(pk=2).delete()
    response = self.client.get('http://localhost:8000/api/theaters/count')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, 1)

    Theater.objects.all().delete()
    response = self.client.get('http://localhost:8000/api/theaters/count')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, 0)