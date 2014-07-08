from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models.activation_token import ActivationToken


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass'
        }
        response_data = {
            'url': url+'1/',
            'username': 'test',
            'email': 'test@test.com',
            'groups': []
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(response.data, response_data)
        user = User.objects.get(username='test')
        self.assertEqual(False, user.is_active)
        token = ActivationToken.objects.get(id=1)
        self.assertEqual(user, token.user)

    def test_activate_account(self):
        """
        Ensure a user can activate his account
        """
        url = '/api/v1/users/'
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass'
        }
        self.client.post(url, data, format='json')
        self.assertEqual(True, ActivationToken.objects.filter(id=1).exists())

        token = ActivationToken.objects.get(id=1)
        data = {'token': token.token}
        url = '/api/v1/users/1/confirm_registration/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username='test')
        self.assertEqual(True, user.is_active)
        self.assertEqual(False, ActivationToken.objects.filter(id=1).exists())
