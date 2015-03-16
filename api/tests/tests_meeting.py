from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase
from core.models import Community, Member, SkillCategory, Request, Location, MeetingPoint, Offer, Meeting, Profile


class MeetingTests(CustomAPITestCase):

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

        profile1 = Profile.objects.create(user=user1)
        profile2 = Profile.objects.create(user=user2)
        profile3 = Profile.objects.create(user=user3)
        profile4 = Profile.objects.create(user=user4)

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

        skill_cat = SkillCategory.objects.create(name='cat', detail='desc')

        request1 = Request.objects.create(user=user1, category=skill_cat, title='help1', detail='det help1', )
        request2 = Request.objects.create(user=user2, category=skill_cat, title='help2', detail='det help2', )
        request3 = Request.objects.create(user=user3, category=skill_cat, title='help3', detail='det help3', )

        offer1= Offer.objects.create(request=request1, user=user3, detail='det off1')
        offer2= Offer.objects.create(request=request2, user=user3, detail='det off2')
        offer3= Offer.objects.create(request=request3, user=user1, detail='det off3')
        offer4= Offer.objects.create(request=request3, user=user2, detail='det off4')

        meeting1 = Meeting.objects.create(offer=offer1, user=user1, status='A', meeting_point=mp1,
                                          date_time='2014-01-01 12:12:12+01')
        meeting2 = Meeting.objects.create(offer=offer2, user=user2, meeting_point=mp2,
                                          date_time='2014-01-01 12:12:12+01')

    def test_valid_setup(self):
        """

        """
        self.assertEqual(4, self.user_model.objects.all().count())
        self.assertEqual(2, Community.objects.all().count())
        self.assertEqual(4, Member.objects.all().count())
        self.assertEqual(2, Location.objects.all().count())
        self.assertEqual(2, MeetingPoint.objects.all().count())
        self.assertEqual(3, Request.objects.all().count())
        self.assertEqual(4, Offer.objects.all().count())
        self.assertEqual(2, Meeting.objects.all().count())

    def test_list_meetings_user1(self):
        """

        """
        url = '/api/v1/meetings/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_list_meetings_user2(self):
        """

        """
        url = '/api/v1/meetings/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_list_meetings_user3(self):
        """

        """
        url = '/api/v1/meetings/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_list_meetings_user4(self):
        """

        """
        url = '/api/v1/meetings/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(0, data['count'])

    def test_create_meeting_not_concerned(self):
        """

        """
        url = '/api/v1/meetings/'
        data = {
            'offer': 4,
            'meeting_point': 1,
            'date_time': '2014-01-01 12:12:12+01',
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Meeting.objects.all().count())

    def test_create_meeting_bad_meeting_point(self):
        """

        """
        url = '/api/v1/meetings/'
        data = {
            'offer': 4,
            'meeting_point': 1,
            'date_time': '2014-01-01 12:12:12+01',
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Meeting.objects.all().count())

    def test_create_meeting(self):
        """

        """
        url = '/api/v1/meetings/'
        data = {
            'offer': 4,
            'meeting_point': 2,
            'date_time': '2014-01-01 12:12:12+01',
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Meeting.objects.all().count())

    def test_validate_meeting_requester(self):
        """

        """
        url = '/api/v1/meetings/1/validate_meeting/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(Meeting.objects.get(id=1).is_validated)

    def test_validate_meeting_helper(self):
        """

        """
        url = '/api/v1/meetings/1/validate_meeting/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(Meeting.objects.get(id=1).is_validated)

    def test_validate_meeting_other(self):
        """

        """
        url = '/api/v1/meetings/1/validate_meeting/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertFalse(Meeting.objects.get(id=1).is_validated)

    def test_accept_meeting_creator(self):
        """

        """
        url = '/api/v1/meetings/2/accept_meeting/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual('P', Meeting.objects.get(id=2).status)

    def test_accept_meeting_non_creator(self):
        """

        """
        url = '/api/v1/meetings/2/accept_meeting/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('A', Meeting.objects.get(id=2).status)
