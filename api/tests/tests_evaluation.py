from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Community, Member, SkillCategory, Request, Location, MeetingPoint, Offer, Meeting, Evaluation
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

        member1 = Member(user=user1, community=community1, role='0', status='1')
        member1.save()
        member2 = Member(user=user2, community=community1, role='1', status='1')
        member2.save()
        member3 = Member(user=user3, community=community1, role='2', status='1')
        member3.save()
        member4 = Member(user=user3, community=community1, role='2', status='1')
        member4.save()

        loc1 = Location(community=community1, name='loc1', description='desc loc 1', gps_x=0.1, gps_y=1.1)
        loc1.save()

        mp1 = MeetingPoint(location=loc1, name='mp1', description='desc mp 1')
        mp1.save()

        skill_cat = SkillCategory(name='cat', detail='desc')
        skill_cat.save()

        request1 = Request(user=user1, category=skill_cat, title='help1', detail='det help1', )
        request1.save()
        request2 = Request(user=user2, category=skill_cat, title='help2', detail='det help2', )
        request2.save()

        offer1= Offer(request=request1, user=user2, detail='det off1')
        offer1.save()
        offer2= Offer(request=request1, user=user3, detail='det off2')
        offer2.save()
        offer3= Offer(request=request2, user=user3, detail='det off3')
        offer3.save()
        offer4= Offer(request=request2, user=user1, detail='det off4')
        offer4.save()

        meeting1 = Meeting(offer=offer1, user=user2, meeting_point=mp1, date_time='2014-01-01 12:12:12+01')
        meeting1.save()
        meeting2 = Meeting(offer=offer2, user=user3, meeting_point=mp1, date_time='2014-01-01 12:12:12+01')
        meeting2.save()
        meeting3 = Meeting(offer=offer3, user=user3, meeting_point=mp1, date_time='2014-01-01 12:12:12+01')
        meeting3.save()
        meeting4 = Meeting(offer=offer4, user=user1, meeting_point=mp1, date_time='2014-01-01 12:12:12+01')
        meeting4.save()

        evaluation1 = Evaluation(meeting=meeting1, mark=1, comment='blabla1')
        evaluation1.save()
        evaluation2 = Evaluation(meeting=meeting2, mark=2, comment='blabla2')
        evaluation2.save()
        evaluation3 = Evaluation(meeting=meeting3, mark=3, comment='blabla3')
        evaluation3.save()

    def test_get_user_evaluation_user1(self):
        """

        """
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/users/1/get_user_evaluation/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({}, response.data)

    def test_get_user_evaluation_user2(self):
        """

        """
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/users/2/get_user_evaluation/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        #self.assertEqual('', response.content)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['average_eval'])
        self.assertEqual(1, data['min_eval'])
        self.assertEqual(1, data['max_eval'])

    def test_get_user_evaluation_user3(self):
        """

        """
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/users/3/get_user_evaluation/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2.5, data['average_eval'])
        self.assertEqual(2, data['min_eval'])
        self.assertEqual(3, data['max_eval'])

    def test_create_evaluation_wrong_user1(self):
        """

        """
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/evaluations/'
        data = {
            'meeting': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_evaluation_wrong_user3(self):
        """

        """
        user = User.objects.get(username="user3")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/evaluations/'
        data = {
            'meeting': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_evaluation_meeting_not_validated(self):
        """

        """
        user = User.objects.get(username="user2")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/evaluations/'
        data = {
            'meeting': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_evaluation_validated_user1(self):
        """

        """
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        m = Meeting.objects.get(id=4)
        m.is_validated = True
        m.save()

        url = '/api/v1/evaluations/'
        data = {
            'meeting': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_evaluation(self):
        """

        """
        user = User.objects.get(username="user2")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        m = Meeting.objects.get(id=4)
        m.is_validated = True
        m.save()

        url = '/api/v1/evaluations/'
        data = {
            'meeting': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_list_evaluations(self):
        """

        """
        user = User.objects.get(username="user3")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/evaluations/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])
        self.assertEqual('Evaluation/2', data['results'][0]['reference'])

