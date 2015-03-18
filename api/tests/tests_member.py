from django.contrib.auth.hashers import make_password
from django.core import mail
from rest_framework import status
from django.contrib.auth.models import User
import time

from api.tests.api_test_case import CustomAPITestCase
from core.models import Member, Community, LocalCommunity, TransportCommunity


class MemberTests(CustomAPITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = self.user_model.objects.create(password=make_password('user1'), email='user1@test.com',
                                               first_name='1', last_name='User', is_active=True)
        moderator = self.user_model.objects.create(password=make_password('user2'), email='user2@test.com',
                                               first_name='2', last_name='User', is_active=True)
        member = self.user_model.objects.create(password=make_password('user3'), email='user3@test.com',
                                               first_name='3', last_name='User', is_active=True)
        other = self.user_model.objects.create(password=make_password('user4'), email='user4@test.com',
                                               first_name='4', last_name='User', is_active=True)

        lcom1 = LocalCommunity.objects.create(name='lcom1', description='descl1', city='Paris', country='FR',
                                              gps_x=0, gps_y=0)
        lcom2 = LocalCommunity.objects.create(name='lcom2', description='descl2', city='Paris', country='FR',
                                              gps_x=0, gps_y=0,
                                              auto_accept_member=True)
        lcom3 = LocalCommunity.objects.create(name='lcom3', description='descl3', city='Paris', country='FR',
                                              gps_x=0, gps_y=0)
        lcom4 = LocalCommunity.objects.create(name='lcom4', description='descl4', city='Paris', country='FR',
                                              gps_x=0, gps_y=0,
                                              auto_accept_member=True)
        lcom5 = LocalCommunity.objects.create(name='lcom5', description='descl5', city='Paris', country='FR',
                                              gps_x=0, gps_y=0)
        tcom1 = TransportCommunity.objects.create(name='tcom1', description='desct1', departure='dep1', arrival='arr1',
                                                  auto_accept_member=True)
        tcom2 = TransportCommunity.objects.create(name='tcom2', description='desct2', departure='dep2', arrival='arr2')
        tcom3 = TransportCommunity.objects.create(name='tcom3', description='desct3', departure='dep3', arrival='arr3')
        tcom4 = TransportCommunity.objects.create(name='tcom4', description='desct4', departure='dep4', arrival='arr4')
        tcom5 = TransportCommunity.objects.create(name='tcom5', description='desct5', departure='dep4', arrival='arr5')

        own_mbr = Member.objects.create(user=owner, community=lcom1, role='0', status='1')
        own_mbr = Member.objects.create(user=owner, community=lcom2, role='0', status='1')

        own_mbr = Member.objects.create(user=owner, community=lcom3, role='0', status='1')
        mod_mbr = Member.objects.create(user=moderator, community=lcom3, role='1', status='0')
        spl_mbr = Member.objects.create(user=member, community=lcom3, role='2', status='0')

        own_mbr = Member.objects.create(user=owner, community=lcom4, role='0', status='1')
        mod_mbr = Member.objects.create(user=moderator, community=lcom4, role='1', status='1')
        spl_mbr = Member.objects.create(user=member, community=lcom4, role='2', status='1')

        own_mbr = Member.objects.create(user=owner, community=lcom5, role='0', status='1')
        spl_mbr = Member.objects.create(user=member, community=lcom5, role='2', status='2')

        own_mbr = Member.objects.create(user=owner, community=tcom1, role='0', status='1')
        own_mbr = Member.objects.create(user=owner, community=tcom2, role='0', status='1')
        own_mbr = Member.objects.create(user=owner, community=tcom3, role='0', status='1')
        own_mbr = Member.objects.create(user=owner, community=tcom4, role='0', status='1')
        own_mbr = Member.objects.create(user=owner, community=tcom5, role='0', status='1')

    def test_setup(self):
        self.assertEqual(4, self.user_model.objects.all().count())
        self.assertEqual(10, Community.objects.all().count())
        self.assertEqual(15, Member.objects.all().count())

    def test_join_wrong_community(self):
        """
        Ensure an authenticated user cannot join a community that does not exists
        """
        url = '/api/v1/communities/15/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        self.assertEqual(15, Member.objects.all().count())

    def test_join_community_not_auto_accept(self):
        """
        Ensure an authenticated user can join a community
        """
        url = '/api/v1/communities/1/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(16, Member.objects.all().count())
        member = Member.objects.get(user=self.user_model.objects.get(id=4))
        community = Community.objects.get(id=1)
        self.assertEqual(community, member.community)
        self.assertEqual("2", member.role)
        self.assertEqual("0", member.status)

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(16, Member.objects.all().count())

    def test_join_community_auto_accept(self):
        """
        Ensure an authenticated user can join a community
        """
        url = '/api/v1/communities/2/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(16, Member.objects.all().count())
        member = Member.objects.get(user=self.user_model.objects.get(id=4))
        community = Community.objects.get(id=2)
        self.assertEqual(community, member.community)
        self.assertEqual("2", member.role)
        self.assertEqual("1", member.status)

    def test_leave_community(self):
        """
        Ensure a member can leave a community
        """
        url = '/api/v1/communities/3/leave_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

        self.assertEqual(14, Member.objects.all().count())

    def test_leave_community_banned(self):
        """
        Ensure a banned member cannot leave a community
        """
        url = '/api/v1/communities/5/leave_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.assertEqual(15, Member.objects.all().count())

    def test_list_my_memberships_without_auth(self):
        """
        Ensure an unauthenticated user cannot list memberships
        """
        url = '/api/v1/communities/0/list_my_memberships/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_my_memberships_member(self):
        """
        Ensure a user can list all his memberships
        """
        url = '/api/v1/communities/0/list_my_memberships/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(3, data['count'])
        self.assertEqual(3, data['results'][0]['community']['id'])
        self.assertEqual(4, data['results'][1]['community']['id'])
        self.assertEqual(5, data['results'][2]['community']['id'])
        self.assertEqual('0', data['results'][0]['status'])
        self.assertEqual('1', data['results'][1]['status'])
        self.assertEqual('2', data['results'][2]['status'])
        self.assertEqual('2', data['results'][0]['role'])
        self.assertEqual('2', data['results'][1]['role'])
        self.assertEqual('2', data['results'][2]['role'])

    def test_list_my_memberships_moderator(self):
        """
        Ensure a user can list all his memberships
        """
        url = '/api/v1/communities/0/list_my_memberships/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(2, data['count'])
        self.assertEqual(3, data['results'][0]['community']['id'])
        self.assertEqual(4, data['results'][1]['community']['id'])
        self.assertEqual('0', data['results'][0]['status'])
        self.assertEqual('1', data['results'][1]['status'])
        self.assertEqual('1', data['results'][0]['role'])
        self.assertEqual('1', data['results'][1]['role'])

    def test_list_my_memberships_owner(self):
        """
        Ensure a user can list all his memberships
        """
        url = '/api/v1/communities/0/list_my_memberships/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(10, data['count'])

    def test_list_members_without_auth(self):
        """
        Ensure non authenticated user cannot list community members
        """
        url = '/api/v1/communities/3/retrieve_members/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_without_member_rights(self):
        """
        Ensure a non-member authenticated user cannot list community members
        """
        url = '/api/v1/communities/3/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user4'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_without_mod_rights(self):
        """
        Ensure a simple user cannot list community members
        """
        url = '/api/v1/communities/3/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user3'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_with_mod_rights_not_accepted(self):
        """
        Ensure a moderator can list community members
        """
        url = '/api/v1/communities/3/retrieve_members/'

        # Test before acceptation
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_with_mod_rights(self):
        """
        Ensure a moderator can list community members
        """
        url = '/api/v1/communities/4/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user2'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(3, data['count'])

        self.assertEqual(6, data['results'][0]['id'])
        self.assertEqual(1, data['results'][0]['user']['id'])
        self.assertEqual('0', data['results'][0]['role'])
        self.assertEqual('1', data['results'][0]['status'])

        self.assertEqual(7, data['results'][1]['id'])
        self.assertEqual(2, data['results'][1]['user']['id'])
        self.assertEqual('1', data['results'][1]['role'])
        self.assertEqual('1', data['results'][1]['status'])

        self.assertEqual(8, data['results'][2]['id'])
        self.assertEqual(3, data['results'][2]['user']['id'])
        self.assertEqual('2', data['results'][2]['role'])
        self.assertEqual('1', data['results'][2]['status'])

    def test_list_members_with_owner_rights(self):
        """
        Ensure an owner can list community members
        """
        url = '/api/v1/communities/4/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user1'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(3, data['count'])

    def test_accept_member_without_auth(self):
        """
        Ensure a non authenticated user can not accept members
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_accept_member_with_simple_member(self):
        """
        Ensure a simple member cannot accept members
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user4'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_accept_member_with_owner(self):
        """
        Ensure an owner can accept members
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(5, data['id'])
        self.assertEqual('1', data['status'])
        time.sleep(1)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject,
                         '[Smartribe] Membership accepted')

    def test_accept_member_with_owner_bad_request(self):
        """
        Ensure accept_member request data format
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'lol': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_accept_member_with_owner_not_found(self):
        """
        Ensure member exists
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 19
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_accept_member_with_not_accepted_moderator(self):
        """
        Ensure an non accepted moderator cannot accept members
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_accept_member_with_moderator(self):
        """
        Ensure an moderator can accept members
        """
        mod = Member.objects.get(id=4)
        mod.status = '1'
        mod.save()

        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(5, data['id'])
        self.assertEqual('1', data['status'])
        time.sleep(1)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject,
                         '[Smartribe] Membership accepted')

    def test_ban_member_without_auth(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_member_with_non_member(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_moderator_with_member(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 7
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_owner_with_member(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 6
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user3'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_member_with_moderator(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(8, data['id'])
        self.assertEqual('2', data['status'])
        time.sleep(1)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject,
                         '[Smartribe] Membership cancelled')

    def test_ban_member_with_owner(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(8, data['id'])
        self.assertEqual('2', data['status'])
        time.sleep(1)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(mail.outbox[0].subject,
                         '[Smartribe] Membership cancelled')

    def test_ban_owner_with_moderator(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 6
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_without_auth(self):
        """

        """
        url = '/api/v1/communities/4/promote_moderator/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_with_user(self):
        """

        """
        url = '/api/v1/communities/4/promote_moderator/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user4'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_with_moderator(self):
        """

        """
        url = '/api/v1/communities/4/promote_moderator/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user2'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_with_owner(self):
        """

        """
        url = '/api/v1/communities/4/promote_moderator/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user1'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(8, data['id'])
        self.assertEqual('1', data['role'])
