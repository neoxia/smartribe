from core.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Profile
from core.models.address import Address
import core.utils


class ProfileTests(APITestCase):
    def setUp(self):
        """
        Make a user for authenticating and
        testing profile actions
        """
        user = User(
            username="test_user",
            password="test",
            email="sd@kjhsq@.ds"
        )
        user.save()
        other_user = User(
            username="other_user",
            password="test",
            email="s@s.id"
        )
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

    def test_create_profile_with_address(self):
        """
        Ensure an  authenticated user can create a profile with an address
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
            'address': {'city': 'Poitiers', 'country': 'France'}
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(True, Address.objects.filter(id=1).exists())
        profile = Profile.objects.get(id=1)
        self.assertEqual('Poitiers', profile.address.city)
        self.assertEqual('France', profile.address.country)

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
            'gender': 'M',
            'address': {'city': 'Poitiers', 'country': 'France'}
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        url = '/api/v1/profiles/1/'
        data = {
            'user': 1,
            #'gender': "M",
            'address': {'city': 'Nantes','country': 'France'}
        }
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Profile.objects.get(id=1).gender, 'M')
        profile = Profile.objects.get(id=1)
        self.assertEqual('Nantes', profile.address.city)

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

    def test_delete_self_profile(self):
        """
        Ensure an authenticated user can modify his profile
        """
        url = '/api/v1/profiles/'
        data = {
            'user': 1,
            'address': {'city': 'Poitiers', 'country': 'France'}
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=self.token_line(), format='json')

        url = '/api/v1/profiles/1/'
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token_line())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(False, Profile.objects.filter(id=1).exists())
        self.assertEqual(False, Address.objects.filter(id=1).exists())

    def test_delete_other_profile(self):
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
        response = self.client.put(url, HTTP_AUTHORIZATION=self.token_line())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
