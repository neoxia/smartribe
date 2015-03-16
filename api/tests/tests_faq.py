from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import length
from rest_framework import status
from django.contrib.auth.models import User
from api.tests.api_test_case import CustomAPITestCase
import core.utils
from core.models import FaqSection, Faq


class FaqTests(CustomAPITestCase):

    user_model = get_user_model()

    def setUp(self):
        """
        Set data
        """
        section = FaqSection.objects.create(title='General')

        faqA = Faq.objects.create(section=section, question='why?', answer='because')
        faqB = Faq.objects.create(section=section, private=True, question='who?', answer='toto')
        faqC = Faq.objects.create(section=section, private=False, question='where?', answer='kitchen')

        user = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)

    def test_list_faq_without_auth(self):
        """
        Ensure an unauthenticated user can only retrieve public answers
        """
        url = '/api/v1/faq/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])
        self.assertEqual(4, length(data['results'][0]))
        self.assertEqual('where?', data['results'][0]['question'])
        self.assertEqual('General', data['results'][0]['section']['title'])

    def test_list_faq_with_auth(self):
        """
        Ensure an authenticated user can retrieve all answers
        """
        url = '/api/v1/faq/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])
