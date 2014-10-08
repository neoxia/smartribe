from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Member, Community, LocalCommunity
import core.utils


class CommunityTests(APITestCase):

    def setUp(self):
        """

        """
        owner = User(username="owner", password="owner", email="owner@test.fr")
        owner.save()
        moderator = User(username="moderator", password="moderator", email="moderator@test.fr")
        moderator.save()
        member = User(username="member", password="member", email="member@test.fr")
        member.save()
        other = User(username="other", password="other", email="other@test.fr")
        other.save()

    def set_create_local_community(self):
        user = User.objects.get(username="owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
            'address': {
                'city': 'city',
                'country': 'country'
            }
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        community = Community.objects.get(id=1)
        mod_mbr = Member(user=User.objects.get(username='moderator'), community=community, role='1', status='1')
        spl_mbr = Member(user=User.objects.get(username='member'), community=community, role='2', status='1')
        mod_mbr.save()
        spl_mbr.save()

    def set_create_local_communities_auto(self):
        user = User.objects.get(username="owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        for num in range(1, 10):
            url = '/api/v1/local_communities/'
            aam = 1
            if num % 2 == 0:
                aam = 0

            data = {
                'name': 'com'+num.__str__(),
                'description': 'com_desc'+num.__str__(),
                'auto_accept_member': aam,
                'address': {
                    'city': 'city'+num.__str__(),
                    'country': 'country'+num.__str__()
                }
            }
            self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

    def test_create_local_community_without_auth(self):
        """
        Ensure we cannot create community
        """
        url = '/api/v1/local_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
            'address': {
                'city': 'city',
                'country': 'country'
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_community_with_auth(self):
        """
        Ensure we can create community when we are authenticated
        """
        # Generate token for community_owner user
        user = User.objects.get(username="owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/'
        data = {
            'name': 'com1',
            'description': 'com1desc',
            'address': {
                'city': 'city',
                'country': 'country'
            }
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Member.objects.all().count())
        self.assertEqual(1, Community.objects.all().count())
        member = Member.objects.get(id=1)
        community = Community.objects.get(id=1)
        self.assertEqual(user, member.user)
        self.assertEqual(community, member.community)
        self.assertEqual("0", member.role)
        self.assertEqual("1", member.status)

    def test_list_local_communities_without_auth(self):
        """
        Ensure a non authenticated user cannot list communities
        """
        self.set_create_local_communities_auto()

        url = '/api/v1/local_communities/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_local_communities_with_auth(self):
        """
        Ensure an authenticated user can list communities
        """
        self.set_create_local_communities_auto()
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(9, data['count'])

    def test_modify_local_community_with_owner(self):
        """
        Ensure a community owner can modify a community
        """
        self.set_create_local_community()
        # Generate token for community_owner user
        user = User.objects.get(username="owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
            'address': {
                'city': 'city',
                'country': 'country'
            }
        }

        response = self.client.put(url, data, HTTP_AUTHORIZATION=auth,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_partial_modify_local_community_with_owner(self):
        """
        Ensure a community owner can partially modify a community
        """
        self.set_create_local_community()

        user = User.objects.get(username="owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/'
        data = {
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_modify_local_community_without_auth(self):
        """
        Ensure a non authenticated user cannot modify a community
        """
        self.set_create_local_community()

        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_local_community_with_simple_user(self):
        """
        Ensure a simple authenticated user cannot modify a community
        """
        self.set_create_local_community()

        user = User.objects.get(username="other")
        token_user = core.utils.gen_auth_token(user)
        auth_user = 'JWT {0}'.format(token_user)

        # Create modification
        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_local_community_with_member(self):
        """
        Ensure a member cannot modify a community
        """
        self.set_create_local_community()

        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        # Create modification
        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_local_community_with_moderator(self):
        """
        Ensure a moderator can modify its community
        """
        self.set_create_local_community()

        user = User.objects.get(username="moderator")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_modify_local_community_with_banned_moderator(self):
        """
        Ensure a banned moderator cannot modify its former community
        """
        self.set_create_local_community()

        user = User.objects.get(username="moderator")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        moderator = Member.objects.get(user=user)
        moderator.status = '2'
        moderator.save()

        # Create modification
        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_local_community_with_moderator(self):
        """
        Ensure a community moderator cannot delete its community
        """
        self.set_create_local_community()

        user = User.objects.get(username="moderator")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(1, LocalCommunity.objects.all().count())
        self.assertEqual(1, Community.objects.all().count())

    def test_delete_local_community_with_owner(self):
        """
        Ensure a community owner can delete its community
        """
        self.set_create_local_community()

        user = User.objects.get(username="owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, LocalCommunity.objects.all().count())
        self.assertEqual(0, Community.objects.all().count())

    def test_list_communities(self):
        """

        """
        self.set_create_local_community()
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual('L', data['results'][0]['type'])
