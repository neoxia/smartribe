import json
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.test import APITestCase
from core.models import PasswordRecovery
from core.models.activation_token import ActivationToken
import core.utils


class AccountTests(APITestCase):

    def token_line(self):
        user = User.objects.get(username="test")
        token = core.utils.gen_auth_token(user)
        return 'JWT {0}'.format(token)

    def create_two_users(self):
        url = '/api/v1/users/'
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass'
        }
        self.client.post(url, data, format='json')
        token = ActivationToken.objects.get(id=1)
        data = {'token': token.token}
        url = '/api/v1/users/1/confirm_registration/'
        self.client.post(url, data, format='json')
        url = '/api/v1/users/'
        data = {
            'username': 'test0',
            'email': 'test0@test.com',
            'password': 'pass0'
        }
        self.client.post(url, data, format='json')

    def create_three_users(self):
        url = '/api/v1/users/'
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass'
        }
        self.client.post(url, data, format='json')
        token = ActivationToken.objects.get(id=1)
        data = {'token': token.token}
        url = '/api/v1/users/1/confirm_registration/'
        self.client.post(url, data, format='json')
        url = '/api/v1/users/'
        data = {
            'username': 'test0',
            'email': 'test0@test.com',
            'password': 'pass0'
        }
        self.client.post(url, data, format='json')
        url = '/api/v1/users/'
        data = {
            'username': 'test1',
            'email': 'test1@test.com',
            'password': 'pass1'
        }
        self.client.post(url, data, format='json')

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

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(True, User.objects.filter(username='test').exists())
        user = User.objects.get(username='test')
        self.assertEqual('test@test.com', user.email)
        self.assertEqual(False, user.is_active)
        self.assertEqual(True, check_password('pass', user.password))
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

    def test_username_is_unique(self):
        """
        Ensure only one account can created with a single username.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'username': 'test',
            'email': 'test1@test.com',
            'password': 'pass1'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, User.objects.filter().count())

    def test_recover_password(self):
        """
        Ensure a user can reset his password.toto
        """
        url = '/api/v1/users/'
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/v1/users/0/recover_password/'
        data = {'email': 'test@test.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = PasswordRecovery.objects.get(user=User.objects.get(email='test@test.com')).token
        url = '/api/v1/users/'+token+'/set_new_password/'
        data = {'password': 'gloup'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, PasswordRecovery.objects.filter().count())
        user = User.objects.get(username='test')
        self.assertEqual(True, check_password('gloup', user.password))

    def test_list_users_without_auth(self):
        """
        Ensure an unauthenticated user cannot list users.
        """
        self.create_two_users()
        url = '/api/v1/users/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_with_auth(self):
        """
        Ensure an authenticated user can list users.
        """
        self.create_three_users()
        url = '/api/v1/users/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO : Finalize test
        data = response.data
        self.assertEqual(3, data['count'])

    def test_search_users(self):
        # TODO : Test search users
        pass

    def test_retrieve_my_user(self):
        """
        Ensure an authenticated user can retrieve his own FULL user.
        """
        root_url = 'http://testserver'
        self.create_two_users()
        url = '/api/v1/users/1/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token_line(), format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(root_url+url, data['url'])
        self.assertEqual('test', data['username'])
        self.assertEqual('test@test.com', data['email'])
        self.assertEqual([], data['groups'])

    def test_retrieve_other_user(self):
        """
        Ensure an authenticated user cannot retrieve a FULL user for other user.
        """
        root_url = 'http://testserver'
        self.create_two_users()
        url = '/api/v1/users/2/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.token_line(), format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(root_url+url, data['url'])
        self.assertEqual('test0', data['username'])
        error = False
        try:
            tmp = data['email']
            tmp = data['groups']
        except:
            error = True
        self.assertEquals(True, error)

    def test_update_my_user(self):
        """
        Ensure an authenticated user can update his own user.
        """
        self.create_two_users()
        url = '/api/v1/users/1/'
        data = {
            'password': 'password'
        }
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(username='test')
        self.assertEqual(True, check_password('password', user.password))

    def test_update_other_user(self):
        """
        Ensure an authenticated user cannot update another user.
        """
        self.create_two_users()
        url = '/api/v1/users/2/'
        data = {
            'password': 'password'
        }
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user = User.objects.get(username='test0')
        self.assertEqual(True, check_password('pass0', user.password))

    def test_delete_my_user(self):
        """
        Ensure an authenticated user can delete his own user.
        """
        self.create_two_users()
        url = '/api/v1/users/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        user = User.objects.filter(username='test').exists()
        self.assertEqual(False, user)

    def test_delete_other_user(self):
        """
        Ensure an authenticated user cannot delete another user.
        """
        self.create_two_users()
        url = '/api/v1/users/2/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user = User.objects.filter(username='test0').exists()
        self.assertEqual(True, user)








