from rest_framework.test import APITestCase

from .models import User
from .serializers import SystemAdminSerializer
from .serializers import TheaterAdminSerializer
from .serializers import UserSerializer

class UserAPITests(APITestCase):
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

  def setUp(self):
    serializer = TheaterAdminSerializer(data=self.test_theater_admin)
    if not serializer.is_valid():
      print(serializer.errors)
    serializer.save()

    serializer = TheaterAdminSerializer(data=self.test_theater_admin2)
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

  def patch(self, user, id):
    return self.client.patch(
      path='http://localhost:8000/api/users/'+id+'/',
      data = user,
      format='json'
    )

  def test_partial_update(self):
    update_user = {
      'name': 'name'
    }

    # user changes the profile info of another user; fail
    self.login(self.test_theater_admin2)
    response = self.patch(update_user,'1')
    self.assertEqual(response.status_code, 403)

    # user changes his profile info; pass
    self.login(self.test_theater_admin)
    response = self.patch(update_user,'1')
    self.assertEqual(response.status_code, 200)
