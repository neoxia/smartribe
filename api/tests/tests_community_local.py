from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Member, Community, LocalCommunity, Address
import core.utils


class LocalCommunityTests(APITestCase):

    def setUp(self):
        """

        """
        owner = User(username="owner", password="owner", email="owner@test.fr")
        moderator = User(username="moderator", password="moderator", email="moderator@test.fr")
        member = User(username="member", password="member", email="member@test.fr")
        other = User(username="other", password="other", email="other@test.fr")
        owner.save()
        moderator.save()
        member.save()
        other.save()

        addr = Address(city='city', country='FR')
        addr.save()

        com1 = LocalCommunity(name='com1', description='desc1', address=addr)
        com2 = LocalCommunity(name='loc1', description='desc2', address=addr, auto_accept_member=True)
        com3 = LocalCommunity(name='loccom1', description='desc3', address=addr)
        com4 = LocalCommunity(name='con2', description='desc4', address=addr)
        com5 = LocalCommunity(name='loc2', description='des5', address=addr)
        com1.save()
        com2.save()
        com3.save()
        com4.save()
        com5.save()

        own_mbr = Member(user=owner, community=com1, role='0', status='1')
        mod_mbr = Member(user=moderator, community=com1, role='1', status='1')
        spl_mbr = Member(user=member, community=com1, role='2', status='1')
        own_mbr.save()
        mod_mbr.save()
        spl_mbr.save()

        own_mbr = Member(user=owner, community=com2, role='0', status='1')
        mod_mbr = Member(user=moderator, community=com2, role='1', status='1')
        spl_mbr = Member(user=member, community=com2, role='2', status='1')
        own_mbr.save()
        mod_mbr.save()
        spl_mbr.save()

    def test_setup(self):
        """
        """
        self.assertEqual(4, User.objects.all().count())
        self.assertEqual(5, LocalCommunity.objects.all().count())
        self.assertEqual(5, Community.objects.all().count())
        self.assertEqual(6, Member.objects.all().count())

    def test_create_local_community_without_auth(self):
        """
        Ensure we cannot create community
        """
        url = '/api/v1/local_communities/'
        data = {
            'name': 'com10',
            'description': 'com1desc',
            'address': {
                'city': 'city',
                'country': 'country'
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(5, Community.objects.all().count())

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
            'name': 'com10',
            'description': 'com1desc',
            'address': {
                'city': 'city',
                'country': 'country'
            }
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(7, Member.objects.all().count())
        self.assertEqual(6, Community.objects.all().count())
        member = Member.objects.get(id=7)
        community = Community.objects.get(id=6)
        self.assertEqual(user, member.user)
        self.assertEqual(community, member.community)
        self.assertEqual("0", member.role)
        self.assertEqual("1", member.status)

    def test_list_local_communities_without_auth(self):
        """
        Ensure a non authenticated user cannot list communities
        """
        url = '/api/v1/local_communities/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_local_communities_with_auth(self):
        """
        Ensure an authenticated user can list communities
        """
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(5, data['count'])

    def test_modify_local_community_with_owner(self):
        """
        Ensure a community owner can modify a community
        """
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

        response = self.client.put(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_partial_modify_local_community_with_owner(self):
        """
        Ensure a community owner can partially modify a community
        """

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
        user = User.objects.get(username="moderator")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        moderator = Member.objects.get(id=2)
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
        user = User.objects.get(username="moderator")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(5, LocalCommunity.objects.all().count())
        self.assertEqual(5, Community.objects.all().count())

    def test_delete_local_community_with_owner(self):
        """
        Ensure a community owner can delete its community
        """
        user = User.objects.get(username="owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(4, LocalCommunity.objects.all().count())
        self.assertEqual(4, Community.objects.all().count())

    def test_list_communities(self):
        """

        """
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(5, data['count'])
        self.assertEqual('L', data['results'][0]['type'])
        self.assertEqual('L', data['results'][1]['type'])
        self.assertEqual('L', data['results'][2]['type'])
        self.assertEqual('L', data['results'][3]['type'])
        self.assertEqual('L', data['results'][4]['type'])

    def test_search_communities_1(self):
        """

        """
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'search': 'loc'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=auth, format='json')
        data = response.data
        self.assertEqual(3, data['count'])

    def test_search_communities_2(self):
        """

        """
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'search': 'com'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=auth)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_search_communities_3(self):
        """

        """
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'search': 'loccom'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=auth)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_search_communities_4(self):
        """

        """
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'search': 'desc'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=auth)
        data = response.data
        self.assertEqual(4, data['count'])

    def test_filter_communities_1(self):
        """

        """
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'name': 'loc1'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=auth)
        data = response.data
        self.assertEqual(1, data['count'])





