from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
import core.utils
from core.models import Inappropriate


class InappropriateTests(APITestCase):

    def setUp(self):
        """
        Set data
        """
        user1 = User(username="test", password="test", email="test@test.com")
        user1.save()

        user2 = User(username="other", password="other", email="other@test.com")
        user2.save()

    def test_create_inappropriate_without_auth(self):
        """
        Ensure an unauthenticated user cannot report inappropriate content
        """
        url = '/api/v1/inappropriates/'
        data = {
            'user': 1,
            'content_url': 'http://testserver.com/api/v1/communities/1/',
            'detail': 'the test'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_inappropriate_with_auth_for_self(self):
        """
        Ensure an authenticated user can report inappropriate content
        """
        user = User.objects.get(username="test")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/inappropriates/'
        data = {
            'user': 1,
            'content_url': 'http://testserver.com/api/v1/communities/1/',
            'detail': 'the test'
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Inappropriate.objects.all().count())
        i = Inappropriate.objects.get(id=1)
        self.assertEqual(user, i.user)
        self.assertEqual('http://testserver.com/api/v1/communities/1/', i.content_url)
        self.assertEqual('the test', i.detail)

    def test_create_inappropriate_with_auth_for_other(self):
        """
        Ensure an authenticated user cannot report inappropriate content for someone else
        """
        user = User.objects.get(username="test")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/inappropriates/'
        data = {
            'user': 2,
            'content_url': 'http://testserver.com/api/v1/communities/1/',
            'detail': 'the test'
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(0, Inappropriate.objects.all().count())
