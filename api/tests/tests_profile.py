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
        # Generate token for user
        user = User.objects.get(username="test_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_bis = Profile.objects.get(id=1).user
        self.assertEqual(user_bis, user)

    def test_create_two_profiles_with_auth(self):
        """
        Ensure an authenticated user cannot create two profiles
        """
        # Generate token for user
        user = User.objects.get(username="test_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/profiles/'
        data = {
            'user': 1,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_profile_for_other(self):
        """
        Ensure an  authenticated user cannot create a profile for someone else
        """
        # Generate token for user
        user = User.objects.get(username="test_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/profiles/'
        data = {
            'user': 2,
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

