from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase
from core.models import Profile


class ProfileTests(CustomAPITestCase):

    user_model = get_user_model()

    def setUp(self):
        """
        Make a user for authenticating and
        testing profile actions
        """

        user1 = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)
        user2 = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)

        profile1 = Profile.objects.create(user=user1, gender='M', city='Poitiers', country='France')

    def test_create_profile_without_auth(self):
        """
        Ensure a non authenticated visitor cannot create a profile
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_profile_with_auth(self):
        """
        Ensure an  authenticated user can create a profile
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 2,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_two_profiles_with_auth(self):
        """
        Ensure an authenticated user cannot create two profiles
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_profile_for_other(self):
        """
        Ensure an authenticated user cannot create a profile for someone else
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 2,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_profile(self):
        """
        Ensure an authenticated user cannot create a profile for someone else
        """
        url = '/api/v1/profiles/1/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertTrue(data['is_early_adopter'])
        self.assertFalse(data['is_donor'])

    def test_modify_self_profile(self):
        """
        Ensure an authenticated user can modify his profile
        """
        url = '/api/v1/profiles/1/'
        data = {
            'user': 1,
            'city': 'Nantes',
            'country': 'France'
        }
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile = Profile.objects.get(id=1)
        self.assertEqual('M', profile.gender)
        self.assertEqual('Nantes', profile.city)

    def test_profile_user_is_readonly(self):
        """
        Ensure an authenticated user can modify his profile
        """
        url = '/api/v1/profiles/1/'
        data = {
            'user': 2,
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        original_user = self.user_model.objects.get(id=1)
        profile_user = Profile.objects.get(id=1).user
        self.assertEqual(original_user, profile_user)

    def test_modify_other_profile(self):
        """
        Ensure an authenticated user can modify his profile
        """

        url = '/api/v1/profiles/1/'
        data = {
            'gender': "F",
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_self_profile(self):
        """
        Ensure an authenticated user can modify his profile
        """
        url = '/api/v1/profiles/1/'
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(False, Profile.objects.filter(id=1).exists())

    def test_delete_other_profile(self):
        """
        Ensure an authenticated user can modify his profile
        """
        url = '/api/v1/profiles/1/'
        response = self.client.put(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_profiles(self):
        """
        """
        p_other = Profile.objects.create(user=self.user_model.objects.get(id=2))

        url = '/api/v1/profiles/'
        data = {
            'user__id': 1
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual(2, Profile.objects.all().count())

