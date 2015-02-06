from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase
from core.models import PasswordRecovery, Profile
from core.models.activation_token import ActivationToken
from core.utils import gen_temporary_token


class AccountTests(CustomAPITestCase):

    def setUp(self):

        user1 = User(username='user1', password=make_password('user1'), email='user1@test.com', is_active=True)
        user2 = User(username='user2', password=make_password('user2'), email='user2@test.com', is_active=False)
        user3 = User(username='user3', password=make_password('user3'), email='user3@test.com', is_active=True)
        user4 = User(username='user4', password=make_password('user4'), email='user4@test.com', is_active=True)
        user5 = User(username='user5', password=make_password('user5'), email='user5@test.com', is_active=False)
        user1.save()
        user2.save()
        user3.save()
        user4.save()
        user5.save()

        profile1 = Profile(user=user1)
        profile2 = Profile(user=user2)
        profile3 = Profile(user=user3)
        profile4 = Profile(user=user4)
        profile5 = Profile(user=user5)
        profile1.save()
        profile2.save()
        profile3.save()
        profile4.save()
        profile5.save()

        act_token1 = ActivationToken(user=user2, token=gen_temporary_token())
        act_token2 = ActivationToken(user=user5, token=gen_temporary_token())
        act_token1.save()
        act_token2.save()

    def test_setup(self):
        self.assertEqual(5, User.objects.all().count())
        self.assertEqual(5, Profile.objects.all().count())
        self.assertEqual(2, ActivationToken.objects.all().count())

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'pass',
            'first_name': 'first',
            'last_name': 'last'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(6, User.objects.all().count())
        self.assertEqual(6, Profile.objects.all().count())

        self.assertTrue(User.objects.filter(username='test').exists())
        user = User.objects.get(username='test')
        self.assertEqual('test@test.com', user.email)
        self.assertEqual('first', user.first_name)
        self.assertEqual('last', user.last_name)
        self.assertFalse(user.is_active)
        self.assertTrue(check_password('pass', user.password))

        token = ActivationToken.objects.get(id=3)
        self.assertEqual(user, token.user)

        profile = Profile.objects.get(id=6)
        self.assertEqual(user, profile.user)

    def test_create_two_accounts_with_same_mail(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'test',
            'email': 'user1@test.com',
            'password': 'pass1',
            'first_name': 'first',
            'last_name': 'last'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(5, User.objects.all().count())

    def test_activate_account(self):
        """
        Ensure a user can activate his account
        """
        token = ActivationToken.objects.get(id=1)
        url = '/api/v1/users/'+token.token+'/confirm_registration/'

        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(username='user2')
        self.assertTrue(user.is_active)
        self.assertFalse(ActivationToken.objects.filter(id=1).exists())

    def test_username_is_unique(self):
        """
        Ensure only one account can created with a single username.
        """
        url = '/api/v1/users/'
        data = {
            'username': 'user1',
            'email': 'test@test.com',
            'password': 'pass1',
            'first_name': 'first',
            'last_name': 'last'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(5, User.objects.filter().count())

    def test_recover_password(self):
        """
        Ensure a user can reset his password.
        """
        url = '/api/v1/users/0/recover_password/'
        data = {'email': 'user1@test.com'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = PasswordRecovery.objects.get(user=User.objects.get(email='user1@test.com')).token
        url = '/api/v1/users/'+token+'/set_new_password/'
        data = {'password': 'gloup'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(0, PasswordRecovery.objects.filter().count())
        user = User.objects.get(username='user1')
        self.assertEqual(True, check_password('gloup', user.password))

    def test_list_users_without_auth(self):
        """
        Ensure an unauthenticated user cannot list users.
        """
        url = '/api/v1/users/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_users_with_auth(self):
        """
        Ensure an authenticated user can list users with public information only.
        """
        url = '/api/v1/users/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(5, data['count'])
        self.assertEqual('user1', data['results'][0]['username'])
        self.assertEqual('user2', data['results'][1]['username'])
        self.assertEqual('user3', data['results'][2]['username'])
        self.assertEqual('user4', data['results'][3]['username'])
        self.assertEqual('user5', data['results'][4]['username'])

    def test_email_not_in_list(self):
        """  """
        url = '/api/v1/users/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertNotIn('email', data['results'][0])
        self.assertNotIn('email', data['results'][1])
        self.assertNotIn('email', data['results'][2])
        self.assertNotIn('email', data['results'][3])
        self.assertNotIn('email', data['results'][4])

    def test_search_users_1(self):
        """
        Ensure an authenticated user can search users.
        """
        url = '/api/v1/users/'

        response = self.client.get(url, {'username': 'user'}, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_users_2(self):
        """  """
        url = '/api/v1/users/'

        response = self.client.get(url, {'username': 'r1'}, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(1, data['count'])

    def test_retrieve_my_user(self):
        """
        Ensure an authenticated user can retrieve his own FULL user.
        """
        url = '/api/v1/users/1/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(1, data['id'])
        self.assertEqual('user1', data['username'])
        self.assertEqual('user1@test.com', data['email'])
        self.assertEqual([], data['groups'])

    def test_retrieve_other_user(self):
        """
        Ensure an authenticated user cannot retrieve a FULL user for other user.
        """
        url = '/api/v1/users/2/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(2, data['id'])
        self.assertEqual('user2', data['username'])
        self.assertNotIn('email', data)
        self.assertNotIn('groups', data)

    def test_update_my_user(self):
        """
        Ensure an authenticated user can update his own user.
        """
        url = '/api/v1/users/1/'
        data = {
            'password': 'password'
        }
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(username='user1')
        self.assertTrue(check_password('password', user.password))

    def test_update_other_user(self):
        """
        Ensure an authenticated user cannot update another user.
        """
        url = '/api/v1/users/3/'
        data = {
            'password': 'password'
        }
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user = User.objects.get(username='user3')
        self.assertTrue(check_password('user3', user.password))

    def test_delete_my_user(self):
        """
        Ensure an authenticated user can delete his own user.
        """
        url = '/api/v1/users/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(User.objects.filter(username='user1').exists())

    def test_delete_other_user(self):
        """
        Ensure an authenticated user cannot delete another user.
        """
        url = '/api/v1/users/2/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(User.objects.filter(username='user2').exists())

    def test_get_my_user_without_auth(self):
        """
        Ensure an unauthenticated user cannot retrieve user information
        """
        url = '/api/v1/users/0/get_my_user/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_my_user_with_auth(self):
        """
        Ensure an authenticated user can retrieve his own information
        """
        url = '/api/v1/users/0/get_my_user/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(1, data['id'])
        self.assertEqual('user1', data['username'])
        self.assertEqual('user1@test.com', data['email'])
        self.assertEqual([], data['groups'])
