from django.contrib.auth.models import User
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase

from core.models import Member, TransportCommunity, Location, Community
import core.utils


class LocationTests(CustomAPITestCase):

    def setUp(self):
        """  """
        user1 = User(username="user1", password="user1", email="user1@test.fr")
        user2 = User(username="user2", password="user2", email="user2@test.fr")
        user3 = User(username="user3", password="user3", email="user3@test.fr")
        user4 = User(username="user4", password="user4", email="user4@test.fr")
        user5 = User(username="user5", password="user5", email="user5@test.fr")
        user6 = User(username="user6", password="user6", email="user6@test.fr")
        user7 = User(username="user7", password="user7", email="user7@test.fr")
        user8 = User(username="user8", password="user8", email="user8@test.fr")
        user1.save()
        user2.save()
        user3.save()
        user4.save()
        user5.save()
        user6.save()
        user7.save()
        user8.save()

        community1 = TransportCommunity(name='community1',
                                        description='description',
                                        auto_accept_member=True,
                                        departure='departure1',
                                        arrival='arrival1')
        community2 = TransportCommunity(name='community2',
                                        description='description',
                                        auto_accept_member=True,
                                        departure='departure2',
                                        arrival='arrival2')
        community3 = TransportCommunity(name='community3',
                                        description='description',
                                        auto_accept_member=True,
                                        departure='departure3',
                                        arrival='arrival3')
        community1.save()
        community2.save()
        community3.save()

        owner1 = Member(user=user1, community=community1, role='0', status='1')
        owner2 = Member(user=user2, community=community2, role='0', status='1')
        owner3 = Member(user=user3, community=community3, role='0', status='1')
        member10 = Member(user=user1, community=community2, role='2', status='1')
        member11 = Member(user=user1, community=community3, role='2', status='1')
        member20 = Member(user=user2, community=community3, role='2', status='1')
        member40 = Member(user=user4, community=community1, role='2', status='1')
        member41 = Member(user=user4, community=community3, role='2', status='1')
        owner1.save()
        owner2.save()
        owner3.save()
        member10.save()
        member11.save()
        member20.save()
        member40.save()
        member41.save()

        location10 = Location(community=community1, name='loc10', description='d',
                              gps_x=0.3, gps_y=1.3, index=0)
        location11 = Location(community=community1, name='loc11', description='d',
                              gps_x=0.3, gps_y=1.3, index=1)
        location12 = Location(community=community1, name='loc12', description='d',
                              gps_x=0.3, gps_y=1.3, index=2)
        location20 = Location(community=community2, name='loc20', description='d',
                              gps_x=0.3, gps_y=1.3, index=0)
        location21 = Location(community=community2, name='loc21', description='d',
                              gps_x=0.3, gps_y=1.3, index=1)
        location30 = Location(community=community3, name='loc30', description='d',
                              gps_x=0.3, gps_y=1.3, index=0)
        location10.save()
        location11.save()
        location12.save()
        location20.save()
        location21.save()
        location30.save()

    def test_valid_setup(self):
        """

        """
        self.assertEqual(8, User.objects.all().count())
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