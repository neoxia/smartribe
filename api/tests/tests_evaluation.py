from django.contrib.auth.models import User
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase
from core.models import Community, Member, SkillCategory, Request, Location, MeetingPoint, Offer, Meeting, Evaluation


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


        evaluation1 = Evaluation(offer=offer1, mark=1, comment='blabla1')
        evaluation1.save()
        evaluation2 = Evaluation(offer=offer2, mark=2, comment='blabla2')
        evaluation2.save()
        evaluation3 = Evaluation(offer=offer3, mark=3, comment='blabla3')
        evaluation3.save()

    def test_get_user_evaluation_user1(self):
        """

        """
        url = '/api/v1/users/1/get_user_evaluation/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({}, response.data)

    def test_get_user_evaluation_user2(self):
        """

        """
        url = '/api/v1/users/2/get_user_evaluation/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        #self.assertEqual('', response.content)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['average_eval'])
        self.assertEqual(1, data['min_eval'])
        self.assertEqual(1, data['max_eval'])

    def test_get_user_evaluation_user3(self):
        """

        """
        url = '/api/v1/users/3/get_user_evaluation/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2.5, data['average_eval'])
        self.assertEqual(2, data['min_eval'])
        self.assertEqual(3, data['max_eval'])

    def test_create_evaluation_wrong_user1(self):
        """

        """
        url = '/api/v1/evaluations/'
        data = {
            'offer': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_evaluation_wrong_user3(self):
        """

        """
        url = '/api/v1/evaluations/'
        data = {
            'offer': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_evaluation_validated_user1(self):
        """

        """
        url = '/api/v1/evaluations/'
        data = {
            'offer': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_evaluation(self):
        """

        """
        self.assertFalse(Offer.objects.get(id=4).closed)
        url = '/api/v1/evaluations/'
        data = {
            'offer': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Offer.objects.get(id=4).closed)

    def test_list_evaluations(self):
        """

        """
        url = '/api/v1/evaluations/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])
        self.assertEqual('Evaluation/2', data['results'][0]['reference'])
        self.assertTrue(data['results'][0]['had_meeting'])
        self.assertEqual('Evaluation/3', data['results'][1]['reference'])
        self.assertFalse(data['results'][1]['had_meeting'])


