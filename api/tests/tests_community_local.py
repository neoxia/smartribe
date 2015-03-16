from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.models import User
from api.tests.api_test_case import CustomAPITestCase
from core.models import Member, Community, LocalCommunity


class LocalCommunityTests(CustomAPITestCase):

    user_model = get_user_model()

    def setUp(self):
        """

        """
        owner = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)
        moderator = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)
        member = self.user_model.objects.create(password=make_password('user3'), email='user3@test.com',
                                               first_name='3', last_name='User', is_active=True)
        other = self.user_model.objects.create(password=make_password('user4'), email='user4@test.com',
                                               first_name='4', last_name='User', is_active=True)


        com1 = LocalCommunity.objects.create(name='com1', description='desc1', city='Paris', country='FR',
                                             gps_x=0, gps_y=0)
        com2 = LocalCommunity.objects.create(name='loc1', description='desc2', city='Paris', country='FR',
                                             gps_x=1, gps_y=1, auto_accept_member=True)
        com3 = LocalCommunity.objects.create(name='loccom1', description='desc3', city='Paris', country='FR',
                                             gps_x=2, gps_y=1)
        com4 = LocalCommunity.objects.create(name='con2', description='desc4', city='Paris', country='FR',
                                             gps_x=3, gps_y=2)
        com5 = LocalCommunity.objects.create(name='loc2', description='des5', city='Paris', country='FR',
                                             gps_x=2, gps_y=3)

        own_mbr = Member.objects.create(user=owner, community=com1, role='0', status='1')
        mod_mbr = Member.objects.create(user=moderator, community=com1, role='1', status='1')
        spl_mbr = Member.objects.create(user=member, community=com1, role='2', status='1')

        own_mbr = Member.objects.create(user=owner, community=com2, role='0', status='1')
        mod_mbr = Member.objects.create(user=moderator, community=com2, role='1', status='1')
        spl_mbr = Member.objects.create(user=member, community=com2, role='2', status='1')

    def test_setup(self):
        """
        """
        self.assertEqual(4, self.user_model.objects.all().count())
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
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.assertEqual(5, Community.objects.all().count())

    def test_create_community_with_auth(self):
        """
        Ensure we can create community when we are authenticated
        """
        url = '/api/v1/local_communities/'
        data = {
            'name': 'com10',
            'description': 'com1desc',
            'city': 'city',
            'country': 'country',
            'gps_x': 0,
            'gps_y': 1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth("user1"), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(7, Member.objects.all().count())
        self.assertEqual(6, Community.objects.all().count())
        member = Member.objects.get(id=7)
        community = Community.objects.get(id=6)
        self.assertEqual(self.user_model.objects.get(email="user1@test.com"), member.user)
        self.assertEqual(community, member.community)
        self.assertEqual("0", member.role)
        self.assertEqual("1", member.status)

    def test_list_local_communities_without_auth(self):
        """
        Ensure a non authenticated user cannot list communities
        """
        url = '/api/v1/local_communities/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_local_communities_with_auth(self):
        """
        Ensure an authenticated user can list communities
        """
        url = '/api/v1/local_communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("user4"))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(5, data['count'])

    def test_modify_local_community_with_owner(self):
        """
        Ensure a community owner can modify a community
        """
        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
            'city': 'city',
            'country': 'country',
            'gps_x': 0,
            'gps_y': 1
        }

        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth("user1"), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_partial_modify_local_community_with_owner(self):
        """
        Ensure a community owner can partially modify a community
        """
        url = '/api/v1/local_communities/1/'
        data = {
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth("user1"), format='json')
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_local_community_with_simple_user(self):
        """
        Ensure a simple authenticated user cannot modify a community
        """
        # Create modification
        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth("user4"), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_local_community_with_member(self):
        """
        Ensure a member cannot modify a community
        """
        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth("user3"), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_local_community_with_moderator(self):
        """
        Ensure a moderator can modify its community
        """
        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth("user2"), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'com1descmodify')

    def test_modify_local_community_with_banned_moderator(self):
        """
        Ensure a banned moderator cannot modify its former community
        """
        moderator = Member.objects.get(id=2)
        moderator.status = '2'
        moderator.save()

        # Create modification
        url = '/api/v1/local_communities/1/'
        data = {
            'name': 'com1',
            'description': 'com1descmodify',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth("user2"), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_local_community_with_moderator(self):
        """
        Ensure a community moderator cannot delete its community
        """
        url = '/api/v1/local_communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth("user2"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(5, LocalCommunity.objects.all().count())
        self.assertEqual(5, Community.objects.all().count())

    def test_delete_local_community_with_owner(self):
        """
        Ensure a community owner can delete its community
        """
        url = '/api/v1/local_communities/1/'

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth("user1"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(4, LocalCommunity.objects.all().count())
        self.assertEqual(4, Community.objects.all().count())

    def test_list_communities_around_me_1(self):
        """
        Ensure a community owner can delete its community
        """
        url = '/api/v1/local_communities/0/list_communities_around_me/'
        data = {
            'gps_x': 2,
            'gps_y': 2,
            'radius': 115
        }

        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(4, data['count'])

    def test_list_communities_around_me_2(self):
        """
        Ensure a community owner can delete its community
        """
        url = '/api/v1/local_communities/0/list_communities_around_me/'
        data = {
            'gps_x': 1,
            'gps_y': 1,
            'radius': 115
        }

        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(3, data['count'])

    def test_list_communities_around_me_3(self):
        """
        Ensure a community owner can delete its community
        """
        url = '/api/v1/local_communities/0/list_communities_around_me/'
        data = {
            'gps_x': 0,
            'gps_y': 0,
            'radius': 115
        }

        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(2, data['count'])
