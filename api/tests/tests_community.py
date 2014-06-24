from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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
        self.assertEqual(response.data, response_data)
