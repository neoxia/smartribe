from rest_framework import status
from django.contrib.auth.models import User

from api.tests.api_test_case import CustomAPITestCase
import core.utils
from core.models import Suggestion


class SuggestionTests(CustomAPITestCase):

    def setUp(self):
        """
        Set data
        """
        user1 = User(username="user", password="user", email="user@test.com")
        user2 = User(username="other", password="other", email="other@test.com")
        user1.save()
        user2.save()

    def test_create_suggestion_without_auth(self):
        """
        Ensure an unauthenticated user cannot post suggestion
        """
        url = '/api/v1/suggestions/'
        data = {
            'category': 'B',
            'user': 1,
            'title': 'test',
            'description': 'the test'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_suggestion_with_auth_for_self(self):
        """
        Ensure an authenticated user can post a suggestion
        """
        url = '/api/v1/suggestions/'
        data = {
            'category': 'B',
            'user': 1,
            'title': 'test',
            'description': 'the test'
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Suggestion.objects.all().count())
        s = Suggestion.objects.get(id=1)
        self.assertEqual('B', s.category)
        self.assertEqual(User.objects.get(username="user"), s.user)
        self.assertEqual('test', s.title)
        self.assertEqual('the test', s.description)

    def test_create_suggestion_with_auth_for_other(self):
        """
        Ensure an authenticated user cannot post a suggestion for someone else
        """
        url = '/api/v1/suggestions/'
        data = {
            'category': 'B',
            'user': 2,
            'title': 'test',
            'description': 'the test'
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(0, Suggestion.objects.all().count())
