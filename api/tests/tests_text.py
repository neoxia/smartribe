from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework import status
from api.tests.api_test_case import CustomAPITestCase
from core.models.text import Text


class TextTests(CustomAPITestCase):

    model = Text
    user_model = get_user_model()

    def setUp(self):

        cache.clear()

        user1 = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)

        self.model.objects.create(tag="TEXT1", content="Text 1", private=False)
        self.model.objects.create(tag="TEXT2", content="Text 2", private=True)

    def test_setup(self):
        self.assertEqual(1, self.user_model.objects.count())
        self.assertEqual(2, self.model.objects.count())

    def test_get_public_text_by_tag_without_auth_OK(self):
        url = "/api/v1/texts/TEXT1/"

        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual("Text 1", data['content'])

    def test_get_public_text_by_tag_without_auth_KO(self):
        url = "/api/v1/texts/TEXT2/"

        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_public_text_by_tag_with_auth_1(self):
        url = "/api/v1/texts/TEXT1/"

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual("Text 1", data['content'])

    def test_get_public_text_by_tag_with_auth_2(self):
        url = "/api/v1/texts/TEXT2/"

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual("Text 2", data['content'])