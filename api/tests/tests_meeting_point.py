from django.contrib.auth.models import User
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase
from core.models import Community, Member, Location, MeetingPoint
import core.utils


class RequestTests(CustomAPITestCase):

    def setUp(self):
        """
        
        """
        user1 = User(username='user1', password='user1', email='user1@test.fr')
        user1.save()
        user2 = User(username='user2', password='user2', email='user2@test.fr')
        user2.save()
        user3 = User(username='user3', password='user3', email='user3@test.fr')
        user3.save()
        user4 = User(username='user4', password='user4', email='user4@test.fr')
        user4.save()

        community1 = Community(name='com1', description='desc1')
        community1.save()
        community2 = Community(name='com2', description='desc2')
        community2.save()

        member1 = Member(user=user1, community=community1, role='0', status='1')
        member1.save()
        member2 = Member(user=user2, community=community2, role='0', status='1')
        member2.save()
        member3 = Member(user=user3, community=community1, role='2', status='1')
        member3.save()
        member4 = Member(user=user3, community=community2, role='2', status='1')
        member4.save()

        loc1 = Location(community=community1, name='loc1', description='desc loc 1', gps_x=0.1, gps_y=1.1)
        loc1.save()
        loc2 = Location(community=community2, name='loc2', description='desc loc 2', gps_x=0.2, gps_y=1.2)
        loc2.save()

        mp1 = MeetingPoint(location=loc1, name='mp1', description='desc mp 1')
        mp1.save()
        mp2 = MeetingPoint(location=loc2, name='mp2', description='desc mp 2')
        mp2.save()
        mp3 = MeetingPoint(location=loc2, name='mp3', description='desc mp 3')
        mp3.save()

    def test_valid_setup(self):
        """

        """
        self.assertEqual(4, User.objects.all().count())
        self.assertEqual(2, Community.objects.all().count())
        self.assertEqual(4, Member.objects.all().count())
        self.assertEqual(2, Location.objects.all().count())
        self.assertEqual(3, MeetingPoint.objects.all().count())

    def test_list_meeting_points_user1(self):
        """

        """
        url = '/api/v1/meeting_points/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_list_meeting_points_user2(self):
        """

        """
        url = '/api/v1/meeting_points/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_list_meeting_points_user3(self):
        """

        """
        url = '/api/v1/meeting_points/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])

    def test_list_meeting_points_user4(self):
        """

        """
        url = '/api/v1/meeting_points/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(0, data['count'])

    def test_create_meeting_point_not_member(self):
        """

        """
        url = '/api/v1/meeting_points/'
        data = {
            'location': 1,
            'name': 'mp',
            'description': 'desc',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user4'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_meeting_point_member_of_community(self):
        """

        """
        url = '/api/v1/meeting_points/'
        data = {
            'location': 1,
            'name': 'mp',
            'description': 'desc',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, MeetingPoint.objects.all().count())

    def test_create_meeting_point_member_of_other_community(self):
        """

        """
        url = '/api/v1/meeting_points/'
        data = {
            'location': 2,
            'name': 'mp',
            'description': 'desc',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_partial_update_meeting_point_not_moderator(self):
        """

        """
        url = '/api/v1/meeting_points/1/'
        data = {
            'description': 'desc bis',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        mp = MeetingPoint.objects.get(id=1)
        self.assertEqual('desc mp 1', mp.description)

    def test_partial_update_meeting_point_moderator(self):
        """

        """
        url = '/api/v1/meeting_points/1/'
        data = {
            'description': 'desc bis',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        mp = MeetingPoint.objects.get(id=1)
        self.assertEqual('desc bis', mp.description)