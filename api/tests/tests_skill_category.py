from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase


class SkillCategoryTests(CustomAPITestCase):

    user_model = get_user_model()

    def setUp(self):
        """
        Make a user for authenticating and
        testing skill actions
        """
        user = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                              first_name='1', last_name='User', is_active=True)
        other = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)

    def test_create_skill_category_without_auth(self):
        """
        Ensure a non authenticated visitor cannot create a skill category
        """
        url = '/api/v1/skill_categories/'
        data = {
            'name': 'doctor',
            'detail': 'test'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
