from rest_framework import status

from django.contrib.auth.models import User
from api.tests.api_test_case import CustomAPITestCase
import core.utils
from core.models import Inappropriate


class InappropriateTests(CustomAPITestCase):

    def setUp(self):
        """
        Set data
        """
        user1 = User(username="test", password="test", email="test@test.com")
        user2 = User(username="other", password="other", email="other@test.com")
        user1.save()
        user2.save()

    def test_create_inappropriate_without_auth(self):
        """
        Ensure an unauthenticated user cannot report inappropriate content
        """
        url = '/api/v1/inappropriates/'
        data = {
            'content_identifier': 'Request/1',
            'detail': 'the test'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_inappropriate_with_auth(self):
        """
        Ensure an authenticated user can report inappropriate content
        """
        url = '/api/v1/inappropriates/'
        data = {
            'content_identifier': 'Request/1',
            'detail': 'the test'
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('test'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Inappropriate.objects.all().count())
        i = Inappropriate.objects.get(id=1)
        self.assertEqual(User.objects.get(username="test"), i.user)
        self.assertEqual('Request/1', i.content_identifier)
        self.assertEqual('the test', i.detail)
