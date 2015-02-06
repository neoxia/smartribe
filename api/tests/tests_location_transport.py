from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from api.tests.api_test_case import CustomAPITestCase

from core.models import Member, TransportCommunity, Location, Community
import core.utils


class LocationTransportCommunityTests(CustomAPITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = User(username="owner", password="owner", email="owner@test.fr")
        moderator = User(username="moderator", password="moderator", email="moderator@test.fr")
        member = User(username="member", password="member", email="member@test.fr")
        other = User(username="other", password="other", email="other@test.fr")
        member.save()
        moderator.save()
        owner.save()
        other.save()

        com1 = TransportCommunity(name='com1', description='com_desc', auto_accept_member=True,
                                  departure='Meudon', arrival='Ivry')
        com2 = TransportCommunity(name='com2', description='com_desc', auto_accept_member=True,
                                  departure='Meudon', arrival='Ivry')
        com3 = TransportCommunity(name='com3', description='com_desc2', auto_accept_member=True,
                                  departure='Meudon', arrival='Ivry')
        com1.save()
        com2.save()
        com3.save()

        own_mbr = Member(user=owner, community=com1, role='0', status='1')
        spl_mbr = Member(user=member, community=com1, role='2', status='1')
        own_mbr.save()
        spl_mbr.save()

        own_mbr = Member(user=owner, community=com2, role='0', status='1')
        spl_mbr = Member(user=member, community=com2, role='2', status='1')
        own_mbr.save()
        spl_mbr.save()

        own_mbr = Member(user=owner, community=com3, role='0', status='1')
        mod_mbr = Member(user=moderator, community=com3, role='1', status='1')
        spl_mbr = Member(user=member, community=com3, role='2', status='1')
        own_mbr.save()
        mod_mbr.save()
        spl_mbr.save()

        loc = Location(community=com2,
                       name='Invalides A', description='description invalides',
                       gps_x=0.6, gps_y=1.6, index=0)
        loc.save()

        loc = Location(community=com3,
                       name='Meudon', description='description meudon',
                       gps_x=0.0, gps_y=1.0, index=0)
        loc.save()
        loc = Location(community=com3,
                       name='Javel', description='description javel',
                       gps_x=0.1, gps_y=1.1, index=1)
        loc.save()
        loc = Location(community=com3,
                       name='Invalides', description='description invalides',
                       gps_x=0.2, gps_y=1.2, index=2)
        loc.save()
        loc = Location(community=com3,
                       name='St Michel', description='description st michel',
                       gps_x=0.3, gps_y=1.3, index=3)
        loc.save()
        loc = Location(community=com3,
                       name='Ivry', description='description ivry',
                       gps_x=0.4, gps_y=1.4, index=4)
        loc.save()

    def test_setup(self):
        self.assertEqual(4, User.objects.all().count())
        self.assertEqual(3, TransportCommunity.objects.all().count())
        self.assertEqual(3, Community.objects.all().count())
        self.assertEqual(7, Member.objects.all().count())
        self.assertEqual(6, Location.objects.all().count())

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
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_first_location_no_index(self):
        """

        """
        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_first_location_negative_index(self):
        """

        """
        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3,
            'index': -1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_first_location_bad_index(self):
        """

        """
        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location',
            'gps_x': 0.3,
            'gps_y': 1.3,
            'index': 1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_first_location(self):
        """

        """
        url = '/api/v1/transport_communities/1/add_location/'
        data = {
            'name': 'Invalides',
            'description': 'description location test',
            'gps_x': 0.3,
            'gps_y': 1.3,
            'index': 0
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(7, Location.objects.all().count())
        loc = Location.objects.get(id=7)
        self.assertEqual(1, loc.community.id)
        self.assertEqual('Invalides', loc.name)
        self.assertEqual('description location test', loc.description)
        self.assertEqual(0.3, loc.gps_x)
        self.assertEqual(1.3, loc.gps_y)
        self.assertEqual(0, loc.index)

    def test_create_second_location_negative_index(self):
        """

        """
        url = '/api/v1/transport_communities/2/add_location/'
        data = {
            'name': 'Javel',
            'description': 'description javel',
            'gps_x': 0.2,
            'gps_y': 1.2,
            'index': -1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        self.assertEqual(6, Location.objects.all().count())

    def test_create_second_location_bad_index(self):
        """

        """
        url = '/api/v1/transport_communities/2/add_location/'
        data = {
            'name': 'Javel',
            'description': 'description javel',
            'gps_x': 0.2,
            'gps_y': 1.2,
            'index': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        self.assertEqual(6, Location.objects.all().count())

    def test_create_second_location_before(self):
        """

        """
        url = '/api/v1/transport_communities/2/add_location/'
        data = {
            'name': 'Javel',
            'description': 'description javel test',
            'gps_x': 0.2,
            'gps_y': 1.2,
            'index': 0
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(7, Location.objects.all().count())

        loc = Location.objects.get(id=1)
        self.assertEqual(2, loc.community.id)
        self.assertEqual('description invalides', loc.description)
        self.assertEqual(0.6, loc.gps_x)
        self.assertEqual(1.6, loc.gps_y)
        self.assertEqual(1, loc.index)

        loc = Location.objects.get(id=7)
        self.assertEqual(2, loc.community.id)
        self.assertEqual('description javel test', loc.description)
        self.assertEqual(0.2, loc.gps_x)
        self.assertEqual(1.2, loc.gps_y)
        self.assertEqual(0, loc.index)

    def test_create_second_location_after(self):
        """

        """
        url = '/api/v1/transport_communities/2/add_location/'
        data = {
            'name': 'St Michel',
            'description': 'description st michel test',
            'gps_x': 0.2,
            'gps_y': 1.2,
            'index': 1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(7, Location.objects.all().count())

        loc = Location.objects.get(id=1)
        self.assertEqual(2, loc.community.id)
        self.assertEqual('description invalides', loc.description)
        self.assertEqual(0.6, loc.gps_x)
        self.assertEqual(1.6, loc.gps_y)
        self.assertEqual(0, loc.index)

        loc = Location.objects.get(id=7)
        self.assertEqual(2, loc.community.id)
        self.assertEqual('description st michel test', loc.description)
        self.assertEqual(0.2, loc.gps_x)
        self.assertEqual(1.2, loc.gps_y)
        self.assertEqual(1, loc.index)

    def test_delete_location_with_member(self):
        """

        """
        url = '/api/v1/transport_communities/3/delete_location/'
        data = {
            'id': 4
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_delete_location_bad_id(self):
        """

        """
        url = '/api/v1/transport_communities/3/delete_location/'
        data = {
            'id': 13
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_location_first(self):
        """

        """
        url = '/api/v1/transport_communities/3/delete_location/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        self.assertEqual(5, Location.objects.all().count())

        loc = Location.objects.get(name='Javel')
        self.assertEqual(0, loc.index)

        loc = Location.objects.get(name='Invalides')
        self.assertEqual(1, loc.index)

        loc = Location.objects.get(name='St Michel')
        self.assertEqual(2, loc.index)

        loc = Location.objects.get(name='Ivry')
        self.assertEqual(3, loc.index)

    def test_delete_location_intermediate(self):
        """

        """
        url = '/api/v1/transport_communities/3/delete_location/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        self.assertEqual(5, Location.objects.all().count())

        loc = Location.objects.get(name='Meudon')
        self.assertEqual(0, loc.index)

        loc = Location.objects.get(name='Javel')
        self.assertEqual(1, loc.index)

        loc = Location.objects.get(name='Invalides')
        self.assertEqual(2, loc.index)

        loc = Location.objects.get(name='Ivry')
        self.assertEqual(3, loc.index)

    def test_delete_location_last(self):
        """

        """
        url = '/api/v1/transport_communities/3/delete_location/'
        data = {
            'id': 6
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        self.assertEqual(5, Location.objects.all().count())

        loc = Location.objects.get(name='Meudon')
        self.assertEqual(0, loc.index)

        loc = Location.objects.get(name='Javel')
        self.assertEqual(1, loc.index)

        loc = Location.objects.get(name='Invalides')
        self.assertEqual(2, loc.index)

        loc = Location.objects.get(name='St Michel')
        self.assertEqual(3, loc.index)
