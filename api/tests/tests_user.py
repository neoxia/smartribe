from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase
from core.models import PasswordRecovery, Profile
from core.models.activation_token import ActivationToken
from core.utils import gen_temporary_token


class AccountTests(CustomAPITestCase):

    model = get_user_model()

    def setUp(self):

        cache.clear()

        user1 = self.model.objects.create(password=make_password('user1'), email='user1@test.com',
                                          first_name='1', last_name='User', is_active=True)
        user2 = self.model.objects.create(password=make_password('user2'), email='user2@test.com',
                                          first_name='2', last_name='User', is_active=False)
        user3 = self.model.objects.create(password=make_password('user3'), email='user3@test.com',
                                          first_name='3', last_name='User', is_active=True)
        user4 = self.model.objects.create(password=make_password('user4'), email='user4@test.com',
                                          first_name='4', last_name='User', is_active=True)
        user5 = self.model.objects.create(password=make_password('user5'), email='user5@test.com',
                                          first_name='5', last_name='User', is_active=False)

        profile1 = Profile.objects.create(user=user1)
        profile2 = Profile.objects.create(user=user2)
        profile3 = Profile.objects.create(user=user3)
        profile4 = Profile.objects.create(user=user4)
        profile5 = Profile.objects.create(user=user5)

        act_token1 = ActivationToken.objects.create(user=user2, token=gen_temporary_token())
        act_token2 = ActivationToken.objects.create(user=user5, token=gen_temporary_token())

    def test_setup(self):
        self.assertEqual(5, self.model.objects.all().count())
        self.assertEqual(3, self.model.objects.filter(is_active=True).count())
        self.assertEqual(2, self.model.objects.filter(is_active=False).count())
        self.assertEqual(5, Profile.objects.all().count())
        self.assertEqual(2, ActivationToken.objects.all().count())

        self.assertTrue(check_password('user1', self.model.objects.get(id=1).password))

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/v1/users/'
        data = {
            'email': 'test@test.com',
            'password': 'pass',
            'first_name': 'first',
            'last_name': 'last'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(6, self.model.objects.all().count())
        self.assertEqual(6, Profile.objects.all().count())
        self.assertEqual(3, ActivationToken.objects.count())

        self.assertTrue(self.model.objects.filter(email='test@test.com').exists())

        user = self.model.objects.get(email='test@test.com')
        self.assertEqual('first', user.first_name)
        self.assertEqual('last', user.last_name)
        self.assertFalse(user.is_active)
        self.assertTrue(check_password('pass', user.password))

        profile = Profile.objects.get(id=6)
        self.assertEqual(user, profile.user)

        token = ActivationToken.objects.get(id=3)
        self.assertEqual(user, token.user)

    def test_create_two_accounts_with_same_mail(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/v1/users/'
        data = {
            'email': 'user1@test.com',
            'password': 'pass1',
            'first_name': 'first',
            'last_name': 'last'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(5, self.model.objects.all().count())

    def test_activate_account(self):
        """
        Ensure a user can activate his account
        """
        token = ActivationToken.objects.get(id=1)
        url = '/api/v1/users/'+token.token+'/confirm_registration/'

        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = self.model.objects.get(email='user2@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(ActivationToken.objects.filter(id=1).exists())

    def test_recover_password(self):
        """
        Ensure a user can reset his password.
        """
        url = '/api/v1/users/0/recover_password/'
        data = {'email': 'user1@test.com'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = PasswordRecovery.objects.get(user=self.model.objects.get(email='user1@test.com')).token
        url = '/api/v1/users/'+token+'/set_new_password/'
        data = {'password': 'gloup'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(0, PasswordRecovery.objects.filter().count())

        user = self.model.objects.get(email='user1@test.com')
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
        self.assertEqual('1', data['results'][0]['first_name'])
        self.assertEqual('2', data['results'][1]['first_name'])
        self.assertEqual('3', data['results'][2]['first_name'])
        self.assertEqual('4', data['results'][3]['first_name'])
        self.assertEqual('5', data['results'][4]['first_name'])

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

        response = self.client.get(url, {'email': 'user'}, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_users_2(self):
        """  """
        url = '/api/v1/users/'

        response = self.client.get(url, {'email': 'r1'}, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
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
        self.assertEqual('user1@test.com', data['email'])
        self.assertEqual('1', data['first_name'])
        self.assertEqual('User', data['last_name'])
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
        self.assertEqual('2', data['first_name'])
        self.assertEqual('User', data['last_name'])
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

        user = self.model.objects.get(email='user1@test.com')
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

        user = self.model.objects.get(email='user3@test.com')
        self.assertTrue(check_password('user3', user.password))

    def test_delete_my_user(self):
        """
        Ensure an authenticated user can delete his own user.
        """
        url = '/api/v1/users/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(self.model.objects.filter(email='user1@test.com').exists())

    def test_delete_other_user(self):
        """
        Ensure an authenticated user cannot delete another user.
        """
        url = '/api/v1/users/2/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(self.model.objects.filter(email='user2@test.com').exists())

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
        self.assertEqual('user1@test.com', data['email'])
        self.assertEqual('1', data['first_name'])
        self.assertEqual('User', data['last_name'])
        self.assertEqual([], data['groups'])

    def test_update_my_password(self):
        """
        Ensure an authenticated user can retrieve his own information
        """
        url = '/api/v1/users/0/update_my_password/'
        data = {
            'password_old': 'user1',
            'password_new': 'newuser1',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        user = self.model.objects.get(id=1)
        self.assertTrue(check_password('newuser1', user.password))
