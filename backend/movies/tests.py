from django.test import TestCase

class MovieViewSetTests(TestCase):
    def test_no_movies(self):
        """
        If no movies exist,...
        """
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, 200)