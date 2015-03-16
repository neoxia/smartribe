from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.models import User
from api.tests.api_test_case import CustomAPITestCase
from core.models import Member, Community, LocalCommunity, TransportCommunity


class CommunityTests(CustomAPITestCase):

    user_model = get_user_model()

    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)
        moderator = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)
        member = self.user_model.objects.create(password=make_password('user3'), email='user3@test.com',
                                               first_name='3', last_name='User', is_active=True)
        other = self.user_model.objects.create(password=make_password('user4'), email='user4@test.com',
                                               first_name='4', last_name='User', is_active=True)

        tcom1 = TransportCommunity.objects.create(name='tcom1', description='desct1',
                                                  departure='dep1', arrival='arr1')
        lcom1 = LocalCommunity.objects.create(name='lcom1', description='descl1', city='Paris', country='FR',
                                              gps_x=0, gps_y=0)
        tcom2 = TransportCommunity.objects.create(name='tcom2', description='desct2',
                                                  departure='dep2', arrival='arr2')
        lcom2 = LocalCommunity.objects.create(name='lcom2', description='descl2', city='Paris', country='FR',
                                              gps_x=0, gps_y=0, auto_accept_member=True)
        lcom3 = LocalCommunity.objects.create(name='lcom3', description='descl3', city='Paris', country='FR',
                                              gps_x=0, gps_y=0)
        tcom3 = TransportCommunity.objects.create(name='tcom3', description='desct3',
                                                  departure='dep3', arrival='arr3')
        tcom4 = TransportCommunity.objects.create(name='tcom4', description='desct4',
                                                  departure='dep4', arrival='arr4')
        lcom4 = LocalCommunity.objects.create(name='lcom4', description='descl4', city='Paris', country='FR',
                                              gps_x=0, gps_y=0)
        lcom5 = LocalCommunity.objects.create(name='lcom5', description='descl5', city='Paris', country='FR',
                                              gps_x=0, gps_y=0)
        tcom5 = TransportCommunity.objects.create(name='tcom5', description='desct5',
                                                  departure='dep4', arrival='arr5')

        own_mbr = Member.objects.create(user=owner, community=lcom2, role='0', status='1')
        mod_mbr = Member.objects.create(user=moderator, community=lcom2, role='1', status='1')
        spl_mbr = Member.objects.create(user=member, community=lcom2, role='2', status='1')

        own_mbr = Member.objects.create(user=owner, community=tcom5, role='0', status='1')
        spl_mbr = Member.objects.create(user=member, community=tcom5, role='2', status='1')

    def test_setup(self):
        """
        """
        self.assertEqual(4, self.user_model.objects.all().count())
        self.assertEqual(5, TransportCommunity.objects.all().count())
        self.assertEqual(5, LocalCommunity.objects.all().count())
        self.assertEqual(10, Community.objects.all().count())
        self.assertEqual(5, Member.objects.all().count())

    def test_list_communities(self):
        """

        """
        url = '/api/v1/communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(10, data['count'])

        self.assertEqual(2, data['results'][0]['id'])
        self.assertEqual('L', data['results'][0]['type'])
        self.assertEqual(4, data['results'][1]['id'])
        self.assertEqual('L', data['results'][1]['type'])
        self.assertEqual(5, data['results'][2]['id'])
        self.assertEqual('L', data['results'][2]['type'])
        self.assertEqual(8, data['results'][3]['id'])
        self.assertEqual('L', data['results'][3]['type'])
        self.assertEqual(9, data['results'][4]['id'])
        self.assertEqual('L', data['results'][4]['type'])
        self.assertEqual(1, data['results'][5]['id'])
        self.assertEqual('T', data['results'][5]['type'])
        self.assertEqual(3, data['results'][6]['id'])
        self.assertEqual('T', data['results'][6]['type'])
        self.assertEqual(6, data['results'][7]['id'])
        self.assertEqual('T', data['results'][7]['type'])
        self.assertEqual(7, data['results'][8]['id'])
        self.assertEqual('T', data['results'][8]['type'])
        self.assertEqual(10, data['results'][9]['id'])
        self.assertEqual('T', data['results'][9]['type'])

    def test_search_communities_1(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'com'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user4"))
        data = response.data
        self.assertEqual(10, data['count'])

    def test_search_communities_2(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'lcom'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user4"))
        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_communities_3(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'tcom'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user4"))
        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_communities_4(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'com2'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user4"))
        data = response.data
        self.assertEqual(2, data['count'])

    def test_search_communities_5(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'descl'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user4"))
        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_communities_6(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'scl2'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user4"))
        data = response.data
        self.assertEqual(1, data['count'])

    def test_retrieve_community_type_and_count_1(self):
        """

        """
        url = '/api/v1/communities/1/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("user4"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual('T', data['type'])
        self.assertEqual(0, data['members_count'])

    def test_retrieve_community_type_and_count_2(self):
        """

        """
        url = '/api/v1/communities/4/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("user4"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual('L', data['type'])
        self.assertEqual(3, data['members_count'])

    def test_retrieve_community_type_and_count_3(self):
        """

        """
        url = '/api/v1/communities/10/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("user4"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual('T', data['type'])
        self.assertEqual(2, data['members_count'])

    def test_am_i_member(self):
        """

        """
        url = '/api/v1/communities/4/am_i_member/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth("user4"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertFalse(data['is_member'])

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth("user1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertTrue(data['is_member'])

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth("user2"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertTrue(data['is_member'])

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth("user3"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertTrue(data['is_member'])

    def test_get_my_membership_owner(self):
        """ """
        url = '/api/v1/communities/4/get_my_membership/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("user1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual('1', data['status'])
        self.assertEqual('0', data['role'])

    def test_get_my_membership_member(self):
        """ """
        url = '/api/v1/communities/4/get_my_membership/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("user3"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual('1', data['status'])
        self.assertEqual('2', data['role'])

    def test_get_my_membership_other(self):
        """ """
        url = '/api/v1/communities/4/get_my_membership/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("user4"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual({}, data)

    def test_get_shared_communities_moderator(self):
        """ """
        url = '/api/v1/communities/0/get_shared_communities/'
        data = {
            'other_user': 2
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual(4, data['results'][0]['id'])


    def test_get_shared_communities_member(self):
        """ """
        url = '/api/v1/communities/0/get_shared_communities/'
        data = {
            'other_user': 3
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(2, data['count'])
        self.assertEqual(4, data['results'][0]['id'])
        self.assertEqual(10, data['results'][1]['id'])

    def test_get_shared_communities_other(self):
        """ """
        url = '/api/v1/communities/0/get_shared_communities/'
        data = {
            'other_user': 4
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("user1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(0, data['count'])
