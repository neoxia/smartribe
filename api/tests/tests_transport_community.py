from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Member, Community, TransportCommunity, TransportStop
import core.utils


class CommunityTests(APITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = User(username="community_owner", password="test", email="z@s.d")
        owner.save()
        moderator = User(username="moderator", password="test0", email="z@s.sd")
        moderator.save()
        user = User(username="simple_user", password="test1", email="zz@ssk.dk")
        user.save()

    def set_create_communities_auto(self):
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        for num in range(1, 10):
            url = '/api/v1/transport_communities/'
            aam = 1
            if num % 2 == 0:
                aam = 0

            data = {
                'name': 'com'+num.__str__(),
                'description': 'com_desc'+num.__str__(),
                'auto_accept_member': aam,
                'transport_stop_departure': {'name': 'departure', 'detail': 'tst'},
                'transport_stop_via': {'name': 'intermediate'},
                'transport_stop_arrival': {'name': 'arrival'},
            }
            self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

    def set_create_transport_community_auto(self):
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
            'transport_stop_departure': {'name': 'departure', 'detail': 'tst'},
            'transport_stop_via': {'name': 'intermediate'},
            'transport_stop_arrival': {'name': 'arrival'},
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

    def test_create_community_without_auth(self):
        """
        Ensure we cannot create community
        """
        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
            'transport_stop_departure': {'name': 'departure', 'detail': 'tst'},
            'transport_stop_via': {'name': 'intermediate'},
            'transport_stop_arrival': {'name': 'arrival'},
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_transport_community_with_auth(self):
        """
        Ensure we can create community when we are authenticated
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
            'transport_stop_departure': {'name': 'departure', 'detail': 'tst'},
            'transport_stop_via': {'name': 'intermediate'},
            'transport_stop_arrival': {'name': 'arrival'},
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Member.objects.all().count())
        self.assertEqual(1, Community.objects.all().count())
        self.assertEqual(1, TransportCommunity.objects.all().count())
        self.assertEqual(3, TransportStop.objects.all().count())
        member = Member.objects.get(id=1)
        community = Community.objects.get(id=1)
        self.assertEqual(user, member.user)
        self.assertEqual(community, member.community)
        self.assertEqual("0", member.role)
        self.assertEqual("1", member.status)

    def test_list_transport_communities_without_auth(self):
        """
        Ensure a non authenticated user cannot list communities
        """
        self.set_create_communities_auto()

        url = '/api/v1/transport_communities/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_transport_communities_with_auth(self):
        """
        Ensure an authenticated user can list communities
        """
        self.set_create_communities_auto()
        user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(9, data['count'])

        url = '/api/v1/communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(9, data['count'])

    def test_modify_transport_community_with_owner(self):
        """
        Ensure a community owner can modify a community
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'com1desc')

        url = '/api/v1/transport_communities/1/'
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

        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['description'], 'com1desc')

        url = '/api/v1/transport_communities/1/'
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
        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

        # Create modification
        url = '/api/v1/transport_communities/1/'
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
        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

        # Create modification
        url = '/api/v1/transport_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_community_with_member(self):
        """
        Ensure a member cannot modify a community
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
        url = '/api/v1/transport_communities/'
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
        url = '/api/v1/transport_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_community_with_moderator(self):
        """
        Ensure a moderator can modify its community
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
        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        # Create moderator
        community = Community.objects.get(name="com1")
        member = Member(user=user, community=community, role=1, status=1)
        member.save()

        # Create modification
        url = '/api/v1/transport_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_modify_community_with_banned_moderator(self):
        """
        Ensure a banned moderator cannot modify its former community
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
        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        # Create banned moderator
        community = Community.objects.get(name="com1")
        member = Member(user=user, community=community, role=1, status=2)
        member.save()

        # Create modification
        url = '/api/v1/transport_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_community_with_moderator(self):
        """
        Ensure a community moderator cannot delete its community
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)
        # Generate token for simple_user user
        user = User.objects.get(username="simple_user")
        token_user = core.utils.gen_auth_token(user)
        auth_user = 'JWT {0}'.format(token_user)
        # Create community
        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        # Create moderator
        community = Community.objects.get(name="com1")
        member = Member(user=user, community=community, role=1, status=1)
        member.save()

        url = '/api/v1/transport_communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=auth_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_community_with_owner(self):
        """
        Ensure a community owner can delete its community
        """
        # Generate token for community_owner user
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)
        # Create community
        url = '/api/v1/transport_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

        url = '/api/v1/transport_communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
