from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase

from core.models import Member, TransportCommunity, Location, Community
import core.utils


class LocationTests(CustomAPITestCase):

    def setUp(self):
        """  """

        user1 = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)
        user2 = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)
        user3 = self.user_model.objects.create(password=make_password('user3'), email='user3@test.com',
                                               first_name='3', last_name='User', is_active=True)
        user4 = self.user_model.objects.create(password=make_password('user4'), email='user4@test.com',
                                               first_name='4', last_name='User', is_active=True)
        user5 = self.user_model.objects.create(password=make_password('user5'), email='user5@test.com',
                                               first_name='5', last_name='User', is_active=True)


        community1 = TransportCommunity.objects.create(name='community1', description='description',
                                                       auto_accept_member=True,
                                                       departure='departure1', arrival='arrival1')
        community2 = TransportCommunity.objects.create(name='community2', description='description',
                                                       auto_accept_member=True,
                                                       departure='departure2', arrival='arrival2')
        community3 = TransportCommunity.objects.create(name='community3', description='description',
                                                       auto_accept_member=True,
                                                       departure='departure3', arrival='arrival3')

        owner1 = Member.objects.create(user=user1, community=community1, role='0', status='1')
        owner2 = Member.objects.create(user=user2, community=community2, role='0', status='1')
        owner3 = Member.objects.create(user=user3, community=community3, role='0', status='1')
        member10 = Member.objects.create(user=user1, community=community2, role='2', status='1')
        member11 = Member.objects.create(user=user1, community=community3, role='2', status='1')
        member20 = Member.objects.create(user=user2, community=community3, role='2', status='1')
        member40 = Member.objects.create(user=user4, community=community1, role='2', status='1')
        member41 = Member.objects.create(user=user4, community=community3, role='2', status='1')

        location10 = Location.objects.create(community=community1, name='loc10', description='d',
                                             gps_x=0.3, gps_y=1.3, index=0)
        location11 = Location.objects.create(community=community1, name='loc11', description='d',
                                             gps_x=0.3, gps_y=1.3, index=1)
        location12 = Location.objects.create(community=community1, name='loc12', description='d',
                                             gps_x=0.3, gps_y=1.3, index=2)
        location20 = Location.objects.create(community=community2, name='loc20', description='d',
                                             gps_x=0.3, gps_y=1.3, index=0)
        location21 = Location.objects.create(community=community2, name='loc21', description='d',
                                             gps_x=0.3, gps_y=1.3, index=1)
        location30 = Location.objects.create(community=community3, name='loc30', description='d',
                                             gps_x=0.3, gps_y=1.3, index=0)

    def test_valid_setup(self):
        """

        """
        self.assertEqual(5, self.user_model.objects.all().count())
        self.assertEqual(3, Community.objects.all().count())
        self.assertEqual(8, Member.objects.all().count())
        self.assertEqual(6, Location.objects.all().count())

    def test_get_shared_locations_1_2(self):
        """
        """
        url = '/api/v1/locations/0/get_shared_locations/'
        data = {
            'other_user': 2
        }

        response = self.client.get(url, data,  HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])

    def test_get_shared_locations_1_3(self):
        """
        """
        url = '/api/v1/locations/0/get_shared_locations/'
        data = {
            'other_user': 3
        }

        response = self.client.get(url, data,  HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_get_shared_locations_1_4(self):
        """
        """
        url = '/api/v1/locations/0/get_shared_locations/'
        data = {
            'other_user': 4
        }

        response = self.client.get(url, data,  HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(4, data['count'])