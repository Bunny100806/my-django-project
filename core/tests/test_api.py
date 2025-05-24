from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PostAPITest(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='pass')
        self.token = Token.objects.create(user=user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_post(self):
        response = self.client.post('/api/posts/', {
            'title': 'New post',
            'content': 'Hello API'
        })
        self.assertEqual(response.status_code, 201)
