from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Community, Member, SkillCategory, Request, Location, MeetingPoint, Offer, Meeting
import core.utils


class RequestTests(APITestCase):

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

        skill_cat = SkillCategory(name='cat', detail='desc')
        skill_cat.save()

        request1 = Request(user=user1, category=skill_cat, title='help1', detail='det help1', )
        request1.save()
        request2 = Request(user=user2, category=skill_cat, title='help2', detail='det help2', )
        request2.save()
        request3 = Request(user=user3, category=skill_cat, title='help3', detail='det help3', )
        request3.save()

        offer1= Offer(request=request1, user=user3, detail='det off1')
        offer1.save()
        offer2= Offer(request=request2, user=user3, detail='det off2')
        offer2.save()
        offer3= Offer(request=request3, user=user1, detail='det off3')
        offer3.save()
        offer4= Offer(request=request3, user=user2, detail='det off4')
        offer4.save()

        meeting1 = Meeting(offer=offer1, meeting_point=mp1, date_time='2014-01-01 12:12:12+01')
        meeting1.save()
        meeting2 = Meeting(offer=offer2, meeting_point=mp2, date_time='2014-01-01 12:12:12+01')
        meeting2.save()

    def test_valid_setup(self):
        """

        """
        self.assertEqual(4, User.objects.all().count())
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
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_list_meetings_user2(self):
        """

        """
        user = User.objects.get(username="user2")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_list_meetings_user3(self):
        """

        """
        user = User.objects.get(username="user3")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_list_meetings_user4(self):
        """

        """
        user = User.objects.get(username="user4")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(0, data['count'])

    def test_create_meeting_not_concerned(self):
        """

        """
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/'
        data = {
            'offer': 4,
            'meeting_point': 1,
            'date_time': '2014-01-01 12:12:12+01',
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Meeting.objects.all().count())

    def test_create_meeting_bad_meeting_point(self):
        """

        """
        user = User.objects.get(username="user2")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/'
        data = {
            'offer': 4,
            'meeting_point': 1,
            'date_time': '2014-01-01 12:12:12+01',
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(2, Meeting.objects.all().count())

    def test_create_meeting(self):
        """

        """
        user = User.objects.get(username="user2")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/'
        data = {
            'offer': 4,
            'meeting_point': 2,
            'date_time': '2014-01-01 12:12:12+01',
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Meeting.objects.all().count())

    def test_validate_meeting_requester(self):
        """

        """
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/1/validate_meeting/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        #self.assertEqual('', response.content)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(Meeting.objects.get(id=1).is_validated)

    def test_validate_meeting_helper(self):
        """

        """
        user = User.objects.get(username="user3")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/1/validate_meeting/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(Meeting.objects.get(id=1).is_validated)

    def test_validate_meeting_other(self):
        """

        """
        user = User.objects.get(username="user2")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/meetings/1/validate_meeting/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertFalse(Meeting.objects.get(id=1).is_validated)
