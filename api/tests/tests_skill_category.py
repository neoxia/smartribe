from core.models import User
from rest_framework import status
from rest_framework.test import APITestCase
import core.utils


class SkillCategoryTests(APITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing skill actions
        """
        user = User(username="test_user", password="test", email="te@tes.fr")
        user.save()
        other_user = User(username="other_user", password="test@test.fr")
        other_user.save()

    def token_line(self):
        user = User.objects.get(username="test_user")
        token = core.utils.gen_auth_token(user)
        return 'JWT {0}'.format(token)

    def token_line_other(self):
        user = User.objects.get(username="other_user")
        token = core.utils.gen_auth_token(user)
        return 'JWT {0}'.format(token)

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
