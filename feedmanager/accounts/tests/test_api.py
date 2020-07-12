from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='test@test.com', password='testpassword')
        self.key = Token.objects.get(user=self.user).key

    def test_create_user(self):
        """
        Ensure create a new user is created and a valid token is created with it.
        """
        data = {
            'email': 'test@test2.com',
            'password': 'testpassword2',
            'password2': 'testpassword2',
        }
        url = api_reverse('accounts:register')
        response = self.client.post(url, data=data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['token'], token.key)

    def test_login_user(self):
        """
        Ensure a registered user logs in and a valid token is returned to the user.
        """
        data = {
            'username': 'test@test.com',
            'password': 'testpassword',
        }
        url = api_reverse('accounts:login')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.key)
