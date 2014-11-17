import datetime

from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status

from api.tests.api_test_case import CustomAPITestCase
from core.models import SkillCategory, Request, Inappropriate, PasswordRecovery
import core.utils
from smartribe import settings


class AutoCloseTests(CustomAPITestCase):

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
        request2 = Request(user=user1, category=skill_cat, title='help2', detail='det help2',
                           expected_end_date=yesterday, auto_close=False)
        request3 = Request(user=user1, category=skill_cat, title='help3', detail='det help3',
                           expected_end_date=today, auto_close=True)
        request4 = Request(user=user1, category=skill_cat, title='help4', detail='det help4',
                           expected_end_date=today, auto_close=False)
        request5 = Request(user=user1, category=skill_cat, title='help5', detail='det help5',
                           expected_end_date=yesterday-datetime.timedelta(days=1), auto_close=True)
        request1.save()
        request2.save()
        request3.save()
        request4.save()
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


class CleanPrtTests(CustomAPITestCase):

    def setUp(self):
        cache.clear()
        user1 = User(username='user1', password='user1', email='user1@test.fr')
        user2 = User(username='user2', password='user2', email='user2@test.fr')
        user3 = User(username='user3', password='user3', email='user3@test.fr')
        user4 = User(username='user4', password='user4', email='user4@test.fr')
        user1.save()
        user2.save()
        user3.save()
        user4.save()

        prt1 = PasswordRecovery(user=user1, token=core.utils.gen_temporary_token(), ip_address='192.168.0.1')
        prt2 = PasswordRecovery(user=user2, token=core.utils.gen_temporary_token(), ip_address='192.168.0.2')
        prt3 = PasswordRecovery(user=user3, token=core.utils.gen_temporary_token(), ip_address='192.168.0.3')
        prt4 = PasswordRecovery(user=user4, token=core.utils.gen_temporary_token(), ip_address='192.168.0.4')
        prt1.save()
        prt2.save()
        prt3.save()
        prt4.save()

        prt1.request_datetime = timezone.now() - datetime.timedelta(hours=settings.PRT_VALIDITY, minutes=1)
        prt2.request_datetime = timezone.now() - datetime.timedelta(hours=settings.PRT_VALIDITY, minutes=40)
        prt3.request_datetime = timezone.now() - datetime.timedelta(hours=settings.PRT_VALIDITY-1, minutes=59)
        prt1.save()
        prt2.save()
        prt3.save()

    def test_setup(self):
        """
        """
        self.assertEqual(4, User.objects.all().count())
        self.assertEqual(4, PasswordRecovery.objects.all().count())

    def test_clean(self):
        """
        """
        url = '/api/v1/server_actions/clean_password_recovery_tokens/'
        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, PasswordRecovery.objects.all().count())
        self.assertFalse(PasswordRecovery.objects.filter(id=1).exists())
        self.assertFalse(PasswordRecovery.objects.filter(id=2).exists())
        self.assertTrue(PasswordRecovery.objects.filter(id=3).exists())
        self.assertTrue(PasswordRecovery.objects.filter(id=4).exists())


class ManageReportedObjectsTests(CustomAPITestCase):

    def setUp(self):
        """

        """
        cache.clear()
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

        response = self.client.post(url, REMOTE_ADDR='192.168.161.12')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject,
                         '[SmarTribe] Inappropriate content warning : tests0')
        self.assertEqual(mail.outbox[1].subject,
                         '[SmarTribe] Inappropriate content warning : tests1')

    def test_manage_twice(self):
        """  """
        url = '/api/v1/server_actions/manage_reported_objects/'

        response = self.client.post(url, REMOTE_ADDR='192.168.161.12')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.post(url, REMOTE_ADDR='192.168.161.12')
        self.assertEqual(status.HTTP_429_TOO_MANY_REQUESTS, response.status_code)
