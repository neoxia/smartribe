from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase
from core.models import Community, Member, SkillCategory, Request, Location, MeetingPoint, Offer, Meeting, Evaluation


class EvaluationTests(CustomAPITestCase):

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

        community1 = Community.objects.create(name='com1', description='desc1')
        community1.save()

        member1 = Member.objects.create(user=user1, community=community1, role='0', status='1')
        member2 = Member.objects.create(user=user2, community=community1, role='1', status='1')
        member3 = Member.objects.create(user=user3, community=community1, role='2', status='1')
        member4 = Member.objects.create(user=user3, community=community1, role='2', status='1')

        loc1 = Location.objects.create(community=community1, name='loc1', description='desc loc 1',
                                       gps_x=0.1, gps_y=1.1)

        mp1 = MeetingPoint.objects.create(location=loc1, name='mp1', description='desc mp 1')

        skill_cat = SkillCategory.objects.create(name='cat', detail='desc')

        request1 = Request.objects.create(user=user1, category=skill_cat, title='help1', detail='det help1', )
        request2 = Request.objects.create(user=user2, category=skill_cat, title='help2', detail='det help2', )

        offer1= Offer.objects.create(request=request1, user=user2, detail='det off1')
        offer2= Offer.objects.create(request=request1, user=user3, detail='det off2')
        offer3= Offer.objects.create(request=request2, user=user3, detail='det off3')
        offer4= Offer.objects.create(request=request2, user=user1, detail='det off4')

        meeting1 = Meeting.objects.create(offer=offer1, user=user2, meeting_point=mp1,
                                          date_time='2014-01-01 12:12:12+01')
        meeting2 = Meeting.objects.create(offer=offer2, user=user3, meeting_point=mp1,
                                          date_time='2014-01-01 12:12:12+01')


        evaluation1 = Evaluation.objects.create(offer=offer1, mark=1, comment='blabla1')
        evaluation2 = Evaluation.objects.create(offer=offer2, mark=2, comment='blabla2')
        evaluation3 = Evaluation.objects.create(offer=offer3, mark=3, comment='blabla3')

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

    def test_create_and_update_evaluation(self):
        """

        """
        url = '/api/v1/evaluations/'
        data = {
            'offer': 4,
            'mark': 5,
            'comment': 'blabla5',
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        url = '/api/v1/evaluations/4/'
        data = {
            'comment': 'blabla5 modified',
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('blabla5 modified', Evaluation.objects.get(id=4).comment)

    def test_list_evaluations(self):
        """

        """
        url = '/api/v1/evaluations/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])
        self.assertEqual('Evaluation/1', data['results'][0]['reference'])
        self.assertTrue(data['results'][0]['had_meeting'])
        self.assertEqual('Evaluation/2', data['results'][1]['reference'])
        self.assertTrue(data['results'][1]['had_meeting'])
        self.assertEqual('Evaluation/3', data['results'][2]['reference'])
        self.assertFalse(data['results'][2]['had_meeting'])


