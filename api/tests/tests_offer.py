from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Community, Member, SkillCategory, Request
import core.utils


class OfferTests(APITestCase):

    def setUp(self):
        """

        """
        user1 = User(username='user1', password='user1', email='user1@test.fr')
        user1.save()
        user2 = User(username='user2', password='user2', email='user2@test.fr')
        user2.save()
        user3 = User(username='user3', password='user3', email='user3@test.fr')
        user3.save()
        user4 = User(username='user4', password='user4', email='user4@test.fr')
        user4.save()
        user5 = User(username='user5', password='user5', email='user5@test.fr')
        user5.save()

        community1 = Community(name='com1', description='desc1')
        community1.save()
        community2 = Community(name='com2', description='desc2')
        community2.save()

        skill_cat = SkillCategory(name='cat', detail='desc')
        skill_cat.save()

        member1 = Member(user=user1, community=community1, role='2', status='1')
        member1.save()
        member2 = Member(user=user1, community=community2, role='2', status='1')
        member2.save()
        member3 = Member(user=user2, community=community2, role='2', status='1')
        member3.save()
        member4 = Member(user=user3, community=community1, role='2', status='1')
        member4.save()
        member5 = Member(user=user5, community=community2, role='2', status='1')
        member5.save()

        request1 = Request(user=user1, category=skill_cat, title='help1', detail='det help1', )
        request1.save()
        request2 = Request(user=user1, category=skill_cat, title='help2', detail='det help2', )
        request2.save()
        request3 = Request(user=user2, category=skill_cat, title='help3', detail='det help3', )
        request3.save()
        request4 = Request(user=user2, category=skill_cat, title='help4', detail='det help4', )
        request4.save()
        request5 = Request(user=user3, category=skill_cat, title='help5', detail='det help5', )
        request5.save()

    def test_create_offer_for_other(self):
        """

        """
        user = User.objects.get(username="user1")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/offers/'
        data = {
            'request': 5,
            'user': 2,
            'detail': 'offer'
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_offer_for_not_linked_request(self):
        """

        """
        user = User.objects.get(username="user2")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/offers/'
        data = {
            'request': 5,
            'user': 2,
            'detail': 'offre'
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_create_offer_for_linked_request(self):
        """

        """
        user = User.objects.get(username="user3")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/offers/'
        data = {
            'request': 1,
            'user': 3,
            'detail': 'offre'
        }

        response = self.client.post(url, data,  HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
