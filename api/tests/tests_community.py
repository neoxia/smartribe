from rest_framework import status
from django.contrib.auth.models import User
from api.tests.api_test_case import CustomAPITestCase
from core.models import Member, Community, Address, LocalCommunity, TransportCommunity
import core.utils


class CommunityTests(CustomAPITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = User(username="owner", password="owner", email="owner@test.fr")
        moderator = User(username="moderator", password="moderator", email="moderator@test.fr")
        member = User(username="member", password="member", email="member@test.fr")
        other = User(username="other", password="other", email="other@test.fr")
        owner.save()
        moderator.save()
        member.save()
        other.save()

        lcom1 = LocalCommunity(name='lcom1', description='descl1', city='Paris', country='FR', gps_x=0, gps_y=0)
        lcom2 = LocalCommunity(name='lcom2', description='descl2', city='Paris', country='FR', gps_x=0, gps_y=0,
                               auto_accept_member=True)
        lcom3 = LocalCommunity(name='lcom3', description='descl3', city='Paris', country='FR', gps_x=0, gps_y=0)
        lcom4 = LocalCommunity(name='lcom4', description='descl4', city='Paris', country='FR', gps_x=0, gps_y=0)
        lcom5 = LocalCommunity(name='lcom5', description='descl5', city='Paris', country='FR', gps_x=0, gps_y=0)
        tcom1 = TransportCommunity(name='tcom1', description='desct1', departure='dep1', arrival='arr1')
        tcom2 = TransportCommunity(name='tcom2', description='desct2', departure='dep2', arrival='arr2')
        tcom3 = TransportCommunity(name='tcom3', description='desct3', departure='dep3', arrival='arr3')
        tcom4 = TransportCommunity(name='tcom4', description='desct4', departure='dep4', arrival='arr4')
        tcom5 = TransportCommunity(name='tcom5', description='desct5', departure='dep4', arrival='arr5')
        tcom1.save()
        lcom1.save()
        tcom2.save()
        lcom2.save()
        lcom3.save()
        tcom3.save()
        tcom4.save()
        lcom4.save()
        lcom5.save()
        tcom5.save()

        own_mbr = Member(user=owner, community=lcom2, role='0', status='1')
        mod_mbr = Member(user=moderator, community=lcom2, role='1', status='1')
        spl_mbr = Member(user=member, community=lcom2, role='2', status='1')
        own_mbr.save()
        mod_mbr.save()
        spl_mbr.save()

        own_mbr = Member(user=owner, community=tcom5, role='0', status='1')
        spl_mbr = Member(user=member, community=tcom5, role='2', status='1')
        own_mbr.save()
        spl_mbr.save()

    def test_setup(self):
        """
        """
        self.assertEqual(4, User.objects.all().count())
        self.assertEqual(5, TransportCommunity.objects.all().count())
        self.assertEqual(5, LocalCommunity.objects.all().count())
        self.assertEqual(10, Community.objects.all().count())
        self.assertEqual(5, Member.objects.all().count())

    def test_list_communities(self):
        """

        """
        url = '/api/v1/communities/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('member'), format='json')
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

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("other"))
        data = response.data
        self.assertEqual(10, data['count'])

    def test_search_communities_2(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'lcom'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("other"))
        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_communities_3(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'tcom'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("other"))
        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_communities_4(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'com2'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("other"))
        data = response.data
        self.assertEqual(2, data['count'])

    def test_search_communities_5(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'descl'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("other"))
        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_communities_6(self):
        """

        """
        url = '/api/v1/communities/'
        data = {
            'search': 'scl2'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth("other"))
        data = response.data
        self.assertEqual(1, data['count'])

    def test_retrieve_community_type_and_count_1(self):
        """

        """
        url = '/api/v1/communities/1/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("other"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual('T', data['type'])
        self.assertEqual(0, data['members_count'])

    def test_retrieve_community_type_and_count_2(self):
        """

        """
        url = '/api/v1/communities/4/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("other"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual('L', data['type'])
        self.assertEqual(3, data['members_count'])

    def test_retrieve_community_type_and_count_3(self):
        """

        """
        url = '/api/v1/communities/10/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth("other"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual('T', data['type'])
        self.assertEqual(2, data['members_count'])

    def test_am_i_member(self):
        """

        """
        url = '/api/v1/communities/4/am_i_member/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth("other"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertFalse(data['is_member'])

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth("owner"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertTrue(data['is_member'])

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth("moderator"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertTrue(data['is_member'])

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth("member"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertTrue(data['is_member'])