from django.core import mail
from django.contrib.auth.models import User
from rest_framework import status
import time

from api.tests.api_test_case import CustomAPITestCase
from core.models import Community, Member, SkillCategory, Request, Offer, Profile
from core.models.notification import Notification
import core.utils


class OfferTests(CustomAPITestCase):

    def setUp(self):
        """

        """
        user1 = User(username='user1', password='user1', email='user1@test.fr')
        user2 = User(username='user2', password='user2', email='user2@test.fr')
        user3 = User(username='user3', password='user3', email='user3@test.fr')
        user4 = User(username='user4', password='user4', email='user4@test.fr')
        user5 = User(username='user5', password='user5', email='user5@test.fr')
        user1.save()
        user2.save()
        user3.save()
        user4.save()
        user5.save()

        profile1 = Profile(user=user1)
        profile2 = Profile(user=user2)
        profile3 = Profile(user=user3)
        profile4 = Profile(user=user4)
        profile5 = Profile(user=user5)
        profile1.save()
        profile2.save()
        profile3.save()
        profile4.save()
        profile5.save()

        community1 = Community(name='com1', description='desc1')
        community2 = Community(name='com2', description='desc2')
        community1.save()
        community2.save()

        skill_cat = SkillCategory(name='cat', detail='desc')
        skill_cat.save()

        member1 = Member(user=user1, community=community1, role='2', status='1')
        member2 = Member(user=user1, community=community2, role='2', status='1')
        member3 = Member(user=user2, community=community2, role='2', status='1')
        member4 = Member(user=user3, community=community1, role='2', status='1')
        member5 = Member(user=user5, community=community2, role='2', status='1')
        member1.save()
        member2.save()
        member3.save()
        member4.save()
        member5.save()

        request1 = Request(user=user1, category=skill_cat, title='help1', detail='det help1', )
        request2 = Request(user=user1, category=skill_cat, title='help2', detail='det help2', )
        request3 = Request(user=user2, category=skill_cat, title='help3', detail='det help3', )
        request4 = Request(user=user2, category=skill_cat, title='help4', detail='det help4', )
        request5 = Request(user=user3, category=skill_cat, title='help5', detail='det help5', )
        request1.save()
        request2.save()
        request3.save()
        request4.save()
        request5.save()

        offer1 = Offer(request=request1, user=user2, detail='offer1')
        offer2 = Offer(request=request1, user=user3, detail='offer2')
        offer3 = Offer(request=request1, user=user4, detail='offer3')
        offer4 = Offer(request=request1, user=user5, detail='offer4')
        offer5 = Offer(request=request2, user=user2, detail='offer5')
        offer6 = Offer(request=request2, user=user3, detail='offer6')
        offer7 = Offer(request=request3, user=user4, detail='offer7')
        offer8 = Offer(request=request4, user=user4, detail='offer8')
        offer9 = Offer(request=request4, user=user5, detail='offer9')
        offer1.save()
        offer2.save()
        offer3.save()
        offer4.save()
        offer5.save()
        offer6.save()
        offer7.save()
        offer8.save()
        offer9.save()

    def test_setup(self):
        self.assertEqual(5, User.objects.all().count())
        self.assertEqual(2, Community.objects.all().count())
        self.assertEqual(1, SkillCategory.objects.all().count())
        self.assertEqual(5, Member.objects.all().count())
        self.assertEqual(5, Request.objects.all().count())
        self.assertEqual(9, Offer.objects.all().count())

    def test_request_offer_count_1(self):
        """ """
        url = '/api/v1/requests/1/get_offer_count/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, response.data['count'])

    def test_request_offer_count_2(self):
        """ """
        url = '/api/v1/requests/2/get_offer_count/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, response.data['count'])

    def test_request_offer_count_3(self):
        """ """
        url = '/api/v1/requests/5/get_offer_count/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, response.data['count'])

    def test_create_offer_for_not_linked_request(self):
        """

        """
        url = '/api/v1/offers/'
        data = {
            'request': 5,
            'user': 2,
            'detail': 'offre'
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_offer_for_linked_request(self):
        """

        """
        url = '/api/v1/offers/'
        data = {
            'request': 1,
            'user': 3,
            'detail': 'offre'
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(1, Notification.objects.all().count())
        self.assertEqual('/offers/10/', Notification.objects.get(id=1).link)
        time.sleep(0.2)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject,
                         '[SmarTribe] Nouvelle proposition')

    def test_offers_count_on_request(self):
        """ """
        url = '/api/v1/requests/1/'

        response = self.client.get(url,  HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(4, data['offers_count'])

    def test_offer_closing(self):
        """ """
        url = '/api/v1/requests/1/close_request/'

        response = self.client.post(url,  HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        offers = Offer.objects.filter(request__id=1)
        for offer in offers:
            self.assertTrue(offer.closed)
