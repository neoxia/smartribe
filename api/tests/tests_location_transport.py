from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Member, TransportCommunity, Location
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
        url = '/api/v1/transport_communities/'
        data = {
            'name': 'RER C',
            'description': 'La ligne',
            'auto_accept_member': True,
            'departure': 'Meudon',
            'arrival': 'Ivry'
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        community = TransportCommunity.objects.get(id=1)
        mod_mbr = Member(user=moderator, community=community, role='1', status='1')
        spl_mbr = Member(user=member, community=community, role='2', status='1')
        mod_mbr.save()
        spl_mbr.save()

    def set_one_location(self):
        community = TransportCommunity.objects.get(id=1)
        loc = Location(community=community,
                       name='Invalides',
                       description='description location',
                       gps_x=0.3,
                       gps_y=1.3,
                       index=0)
        loc.save()

    def test_create_first_location_without_auth(self):
        """

        """
        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_first_location_no_index(self):
        """

        """
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_first_location_negative_index(self):
        """

        """
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3,
            'index': -1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_first_location_bad_index(self):
        """

        """
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3,
            'index': 1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_first_location(self):
        """

        """
        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3,
            'index': 0
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Location.objects.all().count())
        loc = Location.objects.get(id=1)
        self.assertEqual(1, loc.community.id)
        self.assertEqual('Invalides', loc.name)
        self.assertEqual('description location', loc.description)
        self.assertEqual(0.3, loc.gps_x)
        self.assertEqual(1.3, loc.gps_y)
        self.assertEqual(0, loc.index)

    def test_create_second_location_negative_index(self):
        """

        """
        self.set_one_location()

        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Javel',
            'description': 'description javel',
            'gps_x': 0.2,
            'gps_y': 1.2,
            'index': -1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(1, Location.objects.all().count())

    def test_create_second_location_bad_index(self):
        """

        """
        self.set_one_location()

        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Javel',
            'description': 'description javel',
            'gps_x': 0.2,
            'gps_y': 1.2,
            'index': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(1, Location.objects.all().count())

    def test_create_second_location_before(self):
        """

        """
        self.set_one_location()

        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Javel',
            'description': 'description javel',
            'gps_x': 0.2,
            'gps_y': 1.2,
            'index': 0
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Location.objects.all().count())

        loc = Location.objects.get(name='Invalides')
        self.assertEqual(1, loc.community.id)
        self.assertEqual('description location', loc.description)
        self.assertEqual(0.3, loc.gps_x)
        self.assertEqual(1.3, loc.gps_y)
        self.assertEqual(1, loc.index)

        loc = Location.objects.get(name='Javel')
        self.assertEqual(1, loc.community.id)
        self.assertEqual('description javel', loc.description)
        self.assertEqual(0.2, loc.gps_x)
        self.assertEqual(1.2, loc.gps_y)
        self.assertEqual(0, loc.index)

    def test_create_second_location_after(self):
        """

        """
        self.set_one_location()

        user = User.objects.get(username="member")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'St Michel',
            'description': 'description st michel',
            'gps_x': 0.2,
            'gps_y': 1.2,
            'index': 1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Location.objects.all().count())

        loc = Location.objects.get(name='Invalides')
        self.assertEqual(1, loc.community.id)
        self.assertEqual('description location', loc.description)
        self.assertEqual(0.3, loc.gps_x)
        self.assertEqual(1.3, loc.gps_y)
        self.assertEqual(0, loc.index)

        loc = Location.objects.get(name='St Michel')
        self.assertEqual(1, loc.community.id)
        self.assertEqual('description st michel', loc.description)
        self.assertEqual(0.2, loc.gps_x)
        self.assertEqual(1.2, loc.gps_y)
        self.assertEqual(1, loc.index)