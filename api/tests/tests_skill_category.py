from django.contrib.auth.models import User
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase


class SkillCategoryTests(CustomAPITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing skill actions
        """
        user = User(username="user", password="user", email="user@test.fr")
        other = User(username="other", password="other", email="other@test.fr")
        user.save()
        other.save()

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
