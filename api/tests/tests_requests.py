from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase
from core.models import Community, Member, SkillCategory, Request, Skill, Profile
import core.utils


class RequestTests(CustomAPITestCase):

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
        user5 = self.user_model.objects.create(password=make_password('user5'), email='user5@test.com',
                                               first_name='5', last_name='User', is_active=True)

        profile1 = Profile.objects.create(user=user1, photo='profiles/user1.jpg')

        community1 = Community.objects.create(name='com1', description='desc1')
        community2 = Community.objects.create(name='com2', description='desc2')

        category1 = SkillCategory.objects.create(name='cat1', detail='desc')
        category2 = SkillCategory.objects.create(name='cat2', detail='desc')
        category3 = SkillCategory.objects.create(name='cat3', detail='desc')
        category4 = SkillCategory.objects.create(name='cat4', detail='desc')

        skill1 = Skill.objects.create(user=user1, category=category1, description='skill desc 1', level=1)
        skill2 = Skill.objects.create(user=user1, category=category2, description='skill desc 2', level=3)
        skill3 = Skill.objects.create(user=user2, category=category1, description='skill desc 3', level=1)
        skill4 = Skill.objects.create(user=user3, category=category1, description='skill desc 4', level=2)
        skill5 = Skill.objects.create(user=user3, category=category2, description='skill desc 5', level=2)
        skill6 = Skill.objects.create(user=user1, category=category2, description='skill desc 2 bis', level=3)

        member1 = Member.objects.create(user=user1, community=community1, role='2', status='1')
        member2 = Member.objects.create(user=user1, community=community2, role='2', status='1')
        member3 = Member.objects.create(user=user2, community=community2, role='2', status='1')
        member4 = Member.objects.create(user=user3, community=community1, role='2', status='1')
        member5 = Member.objects.create(user=user5, community=community2, role='2', status='1')

        request1 = Request.objects.create(user=user1, category=category1, title='help1', detail='det help1', )
        request2 = Request.objects.create(user=user1, category=category2, title='help2', detail='det help2',
                                          community=community1)
        request3 = Request.objects.create(user=user2, category=category1, title='help3', detail='det help3', )
        request4 = Request.objects.create(user=user2, category=category3, title='help4', detail='det help4', )
        request5 = Request.objects.create(user=user3, category=category4, title='help5', detail='det help5', )

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
