from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase
from core.models import Member, LocalCommunity, Location, Community


class LocationLocalCommunityTests(CustomAPITestCase):

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

        com = LocalCommunity.objects.create(name='com', description='com_desc', city='Paris', country='France',
                                            gps_x=0, gps_y=0,
                                            auto_accept_member=True)

        own_mbr = Member.objects.create(user=owner, community=com, role='0', status='1')
        mod_mbr = Member.objects.create(user=moderator, community=com, role='1', status='1')
        spl_mbr = Member.objects.create(user=member, community=com, role='2', status='1')

        loc1 = Location.objects.create(community=com, name='Gare de Lyon', description='Pour le train',
                                       gps_x=0, gps_y=0)
        loc2 = Location.objects.create(community=com, name='Gare Montparnasse', description='Pour le train',
                                       gps_x=0, gps_y=0)
        loc3 = Location.objects.create(community=com, name='Aéroport d\'Orly', description='Pour l\'avion',
                                       gps_x=0, gps_y=0)
        loc4 = Location.objects.create(community=com, name='Opéra', description='Pour le métro',
                                       gps_x=0, gps_y=0)
        loc5 = Location.objects.create(community=com, name='Saint Lazare', description='Pour le métro, pas le train',
                                       gps_x=0, gps_y=0)

    def test_setup(self):
        self.assertEqual(4, self.user_model.objects.all().count())
        self.assertEqual(1, LocalCommunity.objects.all().count())
        self.assertEqual(1, Community.objects.all().count())
        self.assertEqual(3, Member.objects.all().count())
        self.assertEqual(5, Location.objects.all().count())

    def test_create_location_without_auth(self):
        """

        """
        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_location_with_other(self):
        """

        """
        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user4'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_location_with_member(self):
        """

        """
        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        community = Community.objects.get(id=1)
        location = Location.objects.get(id=6)
        self.assertEqual(community, location.community)
        self.assertEqual('Paris', community.localcommunity.city)

    def test_create_location_with_moderator(self):
        """

        """
        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(6, Location.objects.all().count())

    def test_create_location_with_owner(self):
        """

        """
        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(6, Location.objects.all().count())

    def test_create_location_with_wrong_pk(self):
        """

        """
        url = '/api/v1/local_communities/10/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_list_locations_with_member(self):
        """

        """
        url = '/api/v1/local_communities/1/list_locations/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_locations_with_member_1(self):
        """

        """
        url = '/api/v1/local_communities/1/search_locations/'
        data = {
            'search': 'train'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])

    def test_search_locations_with_member_2(self):
        """

        """
        url = '/api/v1/local_communities/1/search_locations/'
        data = {
            'search': 'avion'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_search_locations_with_member_3(self):
        """

        """
        url = '/api/v1/local_communities/1/search_locations/'
        data = {
            'search': 'Gare'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_delete_location_with_member(self):
        """

        """
        url = '/api/v1/local_communities/1/delete_location/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(5, Location.objects.all().count())

    def test_delete_location_with_moderator(self):
        """

        """
        url = '/api/v1/local_communities/1/delete_location/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(4, Location.objects.all().count())

    def test_delete_location_with_owner(self):
        """

        """
        url = '/api/v1/local_communities/1/delete_location/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(4, Location.objects.all().count())
