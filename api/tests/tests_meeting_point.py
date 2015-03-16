from django.contrib.auth.hashers import make_password
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase
from core.models import Community, Member, Location, MeetingPoint, Request, SkillCategory, Offer


class MeetingPointTests(CustomAPITestCase):

    def setUp(self):
        """
        
        """
        user1 = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)
        user2 = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)
        user3 = self.user_model.objects.create(password=make_password('user3'), email='user3@test.com',
                                               first_name='3', last_name='User', is_active=True)
        user4 = self.user_model.objects.create(password=make_password('user4'), email='user4@test.com',
                                               first_name='4', last_name='User', is_active=True)

        skill_cat = SkillCategory.objects.create(name='cat', detail='desc')

        community1 = Community.objects.create(name='com1', description='desc1')
        community2 = Community.objects.create(name='com2', description='desc2')

        member1 = Member.objects.create(user=user1, community=community1, role='0', status='1')
        member2 = Member.objects.create(user=user2, community=community2, role='0', status='1')
        member3 = Member.objects.create(user=user3, community=community1, role='2', status='1')
        member4 = Member.objects.create(user=user3, community=community2, role='2', status='1')

        loc1 = Location.objects.create(community=community1, name='loc1', description='desc loc 1',
                                       gps_x=0.1, gps_y=1.1)
        loc2 = Location.objects.create(community=community2, name='loc2', description='desc loc 2',
                                       gps_x=0.2, gps_y=1.2)

        mp1 = MeetingPoint.objects.create(location=loc1, name='mp1', description='desc mp 1')
        mp2 = MeetingPoint.objects.create(location=loc2, name='mp2', description='desc mp 2')
        mp3 = MeetingPoint.objects.create(location=loc2, name='mp3', description='desc mp 3')

        request1 = Request.objects.create(user=user1, category=skill_cat, title='help1', detail='det help1', )
        request2 = Request.objects.create(user=user3, category=skill_cat, title='help2', detail='det help2', )
        request3 = Request.objects.create(user=user3, community=community2, category=skill_cat, title='help2',
                                          detail='det help2', )

        offer1 = Offer.objects.create(request=request1, user=user3, detail='offer1')
        offer2 = Offer.objects.create(request=request2, user=user2, detail='offer2')
        offer3 = Offer.objects.create(request=request2, user=user1, detail='offer2')
        offer4 = Offer.objects.create(request=request3, user=user2, detail='offer3')

    def test_valid_setup(self):
        """

        """
        self.assertEqual(4, self.user_model.objects.all().count())
        self.assertEqual(1, SkillCategory.objects.all().count())
        self.assertEqual(2, Community.objects.all().count())
        self.assertEqual(4, Member.objects.all().count())
        self.assertEqual(2, Location.objects.all().count())
        self.assertEqual(3, MeetingPoint.objects.all().count())
        self.assertEqual(3, Request.objects.all().count())
        self.assertEqual(4, Offer.objects.all().count())

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

    def test_get_shared_meeting_point_offer2_user1_forbidden(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 2,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_shared_meeting_point_offer1_user1(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 1,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_get_shared_meeting_point_offer1_user3(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 1,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_get_shared_meeting_point_offer2_user2(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 2,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_get_shared_meeting_point_offer2_user3(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 2,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_get_shared_meeting_point_offer3_user1(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 3,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_get_shared_meeting_point_offer3_user3(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 3,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_get_shared_meeting_point_offer4_user2(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 4,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_get_shared_meeting_point_offer4_user3(self):
        """ """
        url = '/api/v1/meeting_points/0/get_shared_meeting_points/'
        data = {
            'offer': 4,
        }

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])