from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Profile
import core.utils


class ProfileTests(APITestCase):
    def setUp(self):
        """
        Make a user for authenticating and
        testing profile actions
        """
        user = User(username="test_user", password="test")
        user.save()
        other_user = User(username="other_user", password="test")
        other_user.save()

    def token_line(self):
        user = User.objects.get(username="test_user")
        token = core.utils.gen_auth_token(user)
        return 'JWT {0}'.format(token)

    def token_line_other(self):
        user = User.objects.get(username="other_user")
        token = core.utils.gen_auth_token(user)
        return 'JWT {0}'.format(token)

    def test_create_profile_without_auth(self):
        """
        Ensure a non authenticated visitor cannot create a profile
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_profile_with_auth(self):
        """
        Ensure an  authenticated user can create a profile
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_two_profiles_with_auth(self):
        """
        Ensure an authenticated user cannot create two profiles
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_profile_for_other(self):
        """
        Ensure an authenticated user cannot create a profile for someone else
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 2,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_self_profile(self):
        """
        Ensure an authenticated user can modify his profile
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        url = '/api/v1/profiles/1/'
        data = {
            'user': 1,
            'gender': "M",
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_user_is_readonly(self):
        """
        Ensure an authenticated user can modify his profile
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        url = '/api/v1/profiles/1/'
        data = {
            'user': 2,
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        original_user = User.objects.get(username="test_user")
        profile_user = Profile.objects.get(id=1).user
        self.assertEqual(original_user, profile_user)

    def test_modify_other_profile(self):
        """
        Ensure an authenticated user can modify his profile
        """
        # Create user profile
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        # Create other_user profile
        url = '/api/v1/profiles/'
        data = {
            'user': 2,
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line_other(), format='json')

        url = '/api/v1/profiles/2/'
        data = {
            'user': 2,
            'gender': "M",
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)