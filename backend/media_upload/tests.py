import os
import tempfile
from PIL import Image as PILImage

from rest_framework.request import Request
from rest_framework.test import APITestCase

from authentication.serializers import AdminSerializer

from .serializers import ImageSerializer


BASE_DIR = os.path.dirname(
  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


class ImageAPITestCase(APITestCase):

  test_fan_zone_admin = {
    'username': 'fanzoneadmin',
    'password': '123456',
    'email': 'admin@test.com',
    'role': 'fan_zone_admin',
  }

  test_theater_admin = {
    'username': 'theateradmin',
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

  media = os.path.join(BASE_DIR, 'media', 'test')

  tmp_img_path = None

  def setUp(self):
    serializer = AdminSerializer(data=self.test_system_admin)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    image = open(os.path.join(self.media, 'theater.jpg'), 'rb')

    request = {
      'kind': 'o',
      'data': image
    }

    response = self.client.post(
      path='http://localhost:8000/api/auth/login/',
      data = {
        'username': self.test_system_admin['username'],
        'password': self.test_system_admin['password']
      },
      format='json'
    )
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])

    response = self.client.post(
      path='http://localhost:8000/api/media/images/',
      data=request,
      format='multipart'
    )
    image.close()
    self.tmp_img_path = os.path.join(BASE_DIR, response.data['data'][1:])

  def tearDown(self):
    os.remove(self.tmp_img_path)

  def test_create(self):
    image = open(os.path.join(self.media, 'theater.jpg'), 'rb')

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

    request = {
      'kind': 'o',
      'data': image
    }

    response = self.client.post(
      path='http://localhost:8000/api/media/images/',
      data=request,
      format='multipart'
    )

    image.close()

    self.assertEqual(response.status_code, 200)

  def test_destroy(self):
    pass

  def test_list(self):
    response = self.client.get('http://localhost:8000/api/media/images/')
    self.assertEqual(response.status_code, 200)

  def test_retrieve(self):
    response = self.client.get('http://localhost:8000/api/media/images/1')
    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.data)

  def test_update(self):
    pass
