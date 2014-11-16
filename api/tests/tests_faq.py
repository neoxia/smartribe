from django.template.defaultfilters import length
from rest_framework import status
from django.contrib.auth.models import User
from api.tests.api_test_case import CustomAPITestCase
import core.utils
from core.models import FaqSection, Faq


class FaqTests(CustomAPITestCase):

    def setUp(self):
        """
        Set data
        """
        section = FaqSection(title='General')
        section.save()

        faqA = Faq(section=section, question='why?', answer='because')
        faqA.save()

        faqB = Faq(section=section, private=True, question='who?', answer='toto')
        faqB.save()

        faqC = Faq(section=section, private=False, question='where?', answer='kitchen')
        faqC.save()

        user = User(username="test", password="test", email="test@test.com")
        user.save()

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

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('test'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(3, data['count'])
