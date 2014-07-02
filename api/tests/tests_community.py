from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Member, Community
import core.utils


class CommunityTests(APITestCase):
    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = User(username="community_owner", password="test")
        owner.save()
        moderator = User(username="moderator", password="test0")
        moderator.save()
        user = User(username="simple_user", password="test1")
        user.save()

    def test_create_community_without_auth(self):
        """
        Ensure we cannot create community
        """
        url = '/api/v1/communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_community_with_auth(self):
        """
        Ensure we can create community when we are authenticated
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_modify_community_with_owner(self):
        """
        Ensure a community owner can modify a community
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'com1desc')

        url = '/api/v1/communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.put(url, data, HTTP_AUTHORIZATION=auth,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_partial_modify_community_with_owner(self):
        """
        Ensure a community owner can partially modify a community
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'com1desc')

        url = '/api/v1/communities/1/'
        data = {
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_modify_community_without_auth(self):
        """
        Ensure a non authenticated user cannot modify a community
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)
        # Create community
        url = '/api/v1/communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

        # Create modification
        url = '/api/v1/communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_community_with_simple_user(self):
        """
        Ensure a simple authenticated user cannot modify a community
        """
        # Generate token for community_owner user
        owner = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(owner)
        auth = 'JWT {0}'.format(token)
        # Generate token for simple_user user
        user = User.objects.get(username="simple_user")
        token_user = core.utils.gen_auth_token(user)
        auth_user = 'JWT {0}'.format(token_user)
        # Create community
        url = '/api/v1/communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

        # Create modification
        url = '/api/v1/communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_community_with_member(self):
        """
        Ensure a simple authenticated user cannot modify a community
        """
        # Generate token for community_owner user
        owner = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(owner)
        auth = 'JWT {0}'.format(token)
        # Generate token for simple_user user
        user = User.objects.get(username="simple_user")
        token_user = core.utils.gen_auth_token(user)
        auth_user = 'JWT {0}'.format(token_user)
        # Create community
        url = '/api/v1/communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        # Create simple member
        community = Community.objects.get(name="com1")
        member = Member(user=user, community=community, role=2, status=1)
        member.save()

        # Create modification
        url = '/api/v1/communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_community_with_owner(self):
        """
        Ensure a community owner can delete its community                       /// TO BE MODIFIED
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
