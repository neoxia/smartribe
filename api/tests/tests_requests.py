from django.contrib.auth.models import User
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase
from core.models import Community, Member, SkillCategory, Request, Skill, Profile
import core.utils


class RequestTests(CustomAPITestCase):

    def setUp(self):
        """
        
        """
        user1 = User(username='user1', password='user1', email='user1@test.fr')
        user2 = User(username='user2', password='user2', email='user2@test.fr')
        user3 = User(username='user3', password='user3', email='user3@test.fr')
        user4 = User(username='user4', password='user4', email='user4@test.fr')
        user5 = User(username='user5', password='user5', email='user5@test.fr')
        user1.save()
        user2.save()
        user3.save()
        user4.save()
        user5.save()

        profile1 = Profile(user=user1, photo='profiles/user1.jpg')
        profile1.save()

        community1 = Community(name='com1', description='desc1')
        community2 = Community(name='com2', description='desc2')
        community1.save()
        community2.save()

        category1 = SkillCategory(name='cat1', detail='desc')
        category2 = SkillCategory(name='cat2', detail='desc')
        category3 = SkillCategory(name='cat3', detail='desc')
        category4 = SkillCategory(name='cat4', detail='desc')
        category1.save()
        category2.save()
        category3.save()
        category4.save()

        skill1 = Skill(user=user1, category=category1, description='skill desc 1', level=1)
        skill2 = Skill(user=user1, category=category2, description='skill desc 2', level=3)
        skill3 = Skill(user=user2, category=category1, description='skill desc 3', level=1)
        skill4 = Skill(user=user3, category=category1, description='skill desc 4', level=2)
        skill5 = Skill(user=user3, category=category2, description='skill desc 5', level=2)
        skill6 = Skill(user=user1, category=category2, description='skill desc 2 bis', level=3)
        skill1.save()
        skill2.save()
        skill3.save()
        skill4.save()
        skill5.save()
        skill6.save()

        member1 = Member(user=user1, community=community1, role='2', status='1')
        member2 = Member(user=user1, community=community2, role='2', status='1')
        member3 = Member(user=user2, community=community2, role='2', status='1')
        member4 = Member(user=user3, community=community1, role='2', status='1')
        member5 = Member(user=user5, community=community2, role='2', status='1')
        member1.save()
        member2.save()
        member3.save()
        member4.save()
        member5.save()

        request1 = Request(user=user1, category=category1, title='help1', detail='det help1', )
        request2 = Request(user=user1, category=category2, title='help2', detail='det help2', community=community1)
        request3 = Request(user=user2, category=category1, title='help3', detail='det help3', )
        request4 = Request(user=user2, category=category3, title='help4', detail='det help4', )
        request5 = Request(user=user3, category=category4, title='help5', detail='det help5', )
        request1.save()
        request2.save()
        request3.save()
        request4.save()
        request5.save()

    def test_list_request_user1(self):
        """

        """
        url = '/api/v1/requests/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(5, data['count'])
        self.assertEqual('profiles/user1.jpg', data['results'][0]['user_photo'])
        self.assertIsNone(data['results'][0]['community_name'])
        self.assertEqual('com1', data['results'][1]['community_name'])
        self.assertEqual('cat1', data['results'][0]['category_name'])

    def test_list_request_user2(self):
        """

        """
        url = '/api/v1/requests/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])

    def test_list_request_user3(self):
        """

        """
        url = '/api/v1/requests/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])

    def test_list_request_user4(self):
        """

        """
        url = '/api/v1/requests/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(0, data['count'])

    def test_list_request_user5(self):
        """

        """
        url = '/api/v1/requests/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user5'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])

    def test_list_my_requests_user1(self):
        """

        """
        url = '/api/v1/requests/0/list_my_requests/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])

    def test_list_my_requests_user5(self):
        """

        """
        url = '/api/v1/requests/0/list_my_requests/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user5'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(0, data['count'])

    def test_close_request(self):
        """

        """
        url = '/api/v1/requests/1/close_request/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertTrue(data['closed'])

    def test_close_request_for_other(self):
        """

        """
        url = '/api/v1/requests/1/close_request/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_suggested_requests_skill_user1(self):
        """ """
        url = '/api/v1/requests/0/list_suggested_requests_skills/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual(3, data['results'][0]['id'])

    def test_list_suggested_requests_skill_user2(self):
        """ """
        url = '/api/v1/requests/0/list_suggested_requests_skills/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual(1, data['results'][0]['id'])

    def test_list_suggested_requests_skill_user3(self):
        """ """
        url = '/api/v1/requests/0/list_suggested_requests_skills/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(2, data['count'])
        self.assertEqual(1, data['results'][0]['id'])
        self.assertEqual(2, data['results'][1]['id'])

    def test_list_community_requests_user1_com1(self):
        """ """
        url = '/api/v1/requests/0/list_community_requests/'
        data = {'community': 1}

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(3, data['count'])
        self.assertEqual(2, data['results'][0]['id'])
        self.assertEqual(1, data['results'][1]['id'])
        self.assertEqual(5, data['results'][2]['id'])

    def test_list_community_requests_user1_no_community(self):
        """ """
        url = '/api/v1/requests/0/list_community_requests/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_list_community_requests_user1_bad_community(self):
        """ """
        url = '/api/v1/requests/0/list_community_requests/'
        data = {'community': 4}

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_list_community_requests_user2_com1(self):
        """ """
        url = '/api/v1/requests/0/list_community_requests/'
        data = {'community': 1}

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual(1, data['results'][0]['id'])

    def test_list_community_requests_user4_com1(self):
        """ """
        url = '/api/v1/requests/0/list_community_requests/'
        data = {'community': 1}

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(0, data['count'])

    def test_list_community_requests_user1_com2(self):
        """ """
        url = '/api/v1/requests/0/list_community_requests/'
        data = {'community': 2}

        response = self.client.get(url, data, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(3, data['count'])
        self.assertEqual(1, data['results'][0]['id'])
        self.assertEqual(3, data['results'][1]['id'])
        self.assertEqual(4, data['results'][2]['id'])
