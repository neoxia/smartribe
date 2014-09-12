from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Member, LocalCommunity, Location, Community
import core.utils


class LocationLocalCommunityTests(APITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = User(username="owner", password="owner", email="owner@test.fr")
        owner.save()
        moderator = User(username="moderator", password="moderator", email="moderator@test.fr")
        moderator.save()
        member = User(username="member", password="member", email="member@test.fr")
        member.save()
        other = User(username="other", password="other", email="other@test.fr")
        other.save()

        token = core.utils.gen_auth_token(owner)
        auth = 'JWT {0}'.format(token)
        url = '/api/v1/local_communities/'
        data = {
            'name': 'com',
            'description': 'com_desc',
            'auto_accept_member': True,
            'address': {
                'city': 'Paris',
                'country': 'France'
            }
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        community = LocalCommunity.objects.get(id=1)
        mod_mbr = Member(user=moderator, community=community, role='1', status='1')
        spl_mbr = Member(user=member, community=community, role='2', status='1')
        mod_mbr.save()
        spl_mbr.save()

    def set_locations(self):
        com = LocalCommunity.objects.get(id=1)
        loc = Location(community=com, name='Gare de Lyon', description='Pour le train', gps_x=0, gps_y=0)
        loc.save()
        loc = Location(community=com, name='Gare Montparnasse', description='Pour le train', gps_x=0, gps_y=0)
        loc.save()
        loc = Location(community=com, name='Aéroport d\'Orly', description='Pour l\'avion', gps_x=0, gps_y=0)
        loc.save()
        loc = Location(community=com, name='Opéra', description='Pour le métro', gps_x=0, gps_y=0)
        loc.save()
        loc = Location(community=com, name='Saint Lazare', description='Pour le métro, pas le train', gps_x=0, gps_y=0)
        loc.save()

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
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_location_with_other(self):
        """

        """
        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_location_with_member(self):
        """

        """
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        community = Community.objects.get(id=1)
        location = Location.objects.get(id=1)
        self.assertEqual(community, location.community)
        self.assertEqual('Paris', community.localcommunity.address.city)

    def test_create_location_with_moderator(self):
        """

        """
        user = User.objects.get(username="moderator")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_location_with_owner(self):
        """

        """
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_location_with_wrong_pk(self):
        """

        """
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/10/add_location/'
        data = {
            'name': 'loc',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_list_locations_with_member(self):
        """

        """
        self.set_locations()
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/list_locations/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(5, data['count'])

    def test_search_locations_with_member_1(self):
        """

        """
        self.set_locations()
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/search_locations/'
        data = {
            'search': 'train'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])

    def test_search_locations_with_member_2(self):
        """

        """
        self.set_locations()
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/search_locations/'
        data = {
            'search': 'avion'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_search_locations_with_member_3(self):
        """

        """
        self.set_locations()
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/search_locations/'
        data = {
            'search': 'Gare'
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_delete_location_with_member(self):
        """

        """
        self.set_locations()
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/delete_location/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(5, Location.objects.all().count())

    def test_delete_location_with_moderator(self):
        """

        """
        self.set_locations()
        user = User.objects.get(username="moderator")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/delete_location/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(4, Location.objects.all().count())

    def test_delete_location_with_owner(self):
        """

        """
        self.set_locations()
        user = User.objects.get(username="owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/delete_location/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(4, Location.objects.all().count())

    def test_igiuehuih(self):
        """

        """

        user = User.objects.get(username="other")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/local_communities/1/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Member.objects.all().count())
        member = Member.objects.get(user=user)
        community = Community.objects.get(id=1)
        self.assertEqual(community, member.community)
        self.assertEqual("2", member.role)
        self.assertEqual("1", member.status)