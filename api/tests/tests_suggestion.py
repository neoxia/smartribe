from django.contrib.auth.hashers import make_password
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
        user1 = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)
        user2 = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)

    def test_create_suggestion_without_auth(self):
        """
        Ensure an unauthenticated user cannot post suggestion
        """
        url = '/api/v1/suggestions/'
        data = {
            'category': 'B',
            'title': 'test',
            'description': 'the test'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_suggestion_with_auth_for_self(self):
        """
        Ensure an authenticated user can post a suggestion
        """
        url = '/api/v1/suggestions/'
        data = {
            'category': 'B',
            'title': 'test',
            'description': 'the test'
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Suggestion.objects.all().count())
        s = Suggestion.objects.get(id=1)
        self.assertEqual('B', s.category)
        self.assertEqual(self.user_model.objects.get(email="user1@test.com"), s.user)
        self.assertEqual('test', s.title)
        self.assertEqual('the test', s.description)
