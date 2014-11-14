import datetime
from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Community, Member, SkillCategory, Request, Inappropriate
import core.utils


class AutoCloseTests(APITestCase):

    def setUp(self):
        """
        
        """
        cache.clear()
        user1 = User(username='user1', password='user1', email='user1@test.fr')
        user1.save()

        skill_cat = SkillCategory(name='cat', detail='desc')
        skill_cat.save()

        today = datetime.date.today()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        request1 = Request(user=user1, category=skill_cat, title='help1', detail='det help1',
                           expected_end_date=yesterday, auto_close=True)
        request1.save()

        request2 = Request(user=user1, category=skill_cat, title='help2', detail='det help2',
                           expected_end_date=yesterday, auto_close=False)
        request2.save()

        request3 = Request(user=user1, category=skill_cat, title='help3', detail='det help3',
                           expected_end_date=today, auto_close=True)
        request3.save()

        request4 = Request(user=user1, category=skill_cat, title='help4', detail='det help4',
                           expected_end_date=today, auto_close=False)
        request4.save()

        request5 = Request(user=user1, category=skill_cat, title='help5', detail='det help5',
                           expected_end_date=yesterday-datetime.timedelta(days=1), auto_close=True)
        request5.save()

    def test_auto_close_requests(self):
        """

        """
        url = '/api/v1/server_actions/auto_close_requests/'

        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(Request.objects.get(id=1).closed)
        self.assertFalse(Request.objects.get(id=2).closed)
        self.assertFalse(Request.objects.get(id=3).closed)
        self.assertFalse(Request.objects.get(id=4).closed)
        self.assertTrue(Request.objects.get(id=5).closed)

    def test_auto_close_requests_twice(self):
        """

        """
        url = '/api/v1/server_actions/auto_close_requests/'

        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        obj = Request.objects.get(id=1)
        self.assertTrue(obj.closed)
        obj.closed = False
        obj.save()

        response = self.client.post(url)
        self.assertEqual(status.HTTP_429_TOO_MANY_REQUESTS, response.status_code)
        obj = Request.objects.get(id=1)
        self.assertFalse(obj.closed)


class CleanPrtTests(APITestCase):

    def setUp(self):
        """

        """


class ManageReportedObjectsTests(APITestCase):

    def setUp(self):
        """

        """
        user = User(username='user', password='user', email='user@test.fr')
        user.save()

        i01 = Inappropriate(user=user, content_identifier='tests1', detail='details')
        i02 = Inappropriate(user=user, content_identifier='tests0', detail='details')
        i03 = Inappropriate(user=user, content_identifier='tests0', detail='details')
        i04 = Inappropriate(user=user, content_identifier='tests1', detail='details')
        i05 = Inappropriate(user=user, content_identifier='tests0', detail='details')
        i06 = Inappropriate(user=user, content_identifier='tests2', detail='details')
        i07 = Inappropriate(user=user, content_identifier='tests1', detail='details')
        i08 = Inappropriate(user=user, content_identifier='tests0', detail='details')
        i09 = Inappropriate(user=user, content_identifier='tests0', detail='details')
        i10 = Inappropriate(user=user, content_identifier='tests2', detail='details')
        i11 = Inappropriate(user=user, content_identifier='tests1', detail='details')
        i12 = Inappropriate(user=user, content_identifier='tests0', detail='details')
        i13 = Inappropriate(user=user, content_identifier='tests2', detail='details')
        i14 = Inappropriate(user=user, content_identifier='tests1', detail='details')
        i01.save()
        i02.save()
        i03.save()
        i04.save()
        i05.save()
        i06.save()
        i07.save()
        i08.save()
        i09.save()
        i10.save()
        i11.save()
        i12.save()
        i13.save()
        i14.save()

    def test_manage(self):
        """

        """
        url = '/api/v1/server_actions/manage_reported_objects/'

        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject,
                         '[SmarTribe] Inappropriate content warning : tests0')

    def test_manage2(self):
        """

        """
        i = Inappropriate(user=User.objects.get(id=1), content_identifier='tests1', detail='details3')
        i.save()

        url = '/api/v1/server_actions/manage_reported_objects/'

        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject,
                         '[SmarTribe] Inappropriate content warning : tests0')
        self.assertEqual(mail.outbox[1].subject,
                         '[SmarTribe] Inappropriate content warning : tests1')
