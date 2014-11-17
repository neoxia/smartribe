from django.core import mail
from rest_framework import status
from django.contrib.auth.models import User

from api.tests.api_test_case import CustomAPITestCase
from core.models import Member, Community, LocalCommunity, TransportCommunity


class MemberTests(CustomAPITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = User(username="owner", password="owner", email="owner@test.com")
        moderator = User(username="moderator", password="moderator", email="moderator@test.com")
        member = User(username="member", password="member", email="member@test.com")
        user = User(username="user", password="user", email="user@test.com")
        owner.save()
        moderator.save()
        member.save()
        user.save()

        lcom1 = LocalCommunity(name='lcom1', description='descl1', city='Paris', country='FR', gps_x=0, gps_y=0)
        lcom2 = LocalCommunity(name='lcom2', description='descl2', city='Paris', country='FR', gps_x=0, gps_y=0,
                               auto_accept_member=True)
        lcom3 = LocalCommunity(name='lcom3', description='descl3', city='Paris', country='FR', gps_x=0, gps_y=0)
        lcom4 = LocalCommunity(name='lcom4', description='descl4', city='Paris', country='FR', gps_x=0, gps_y=0,
                               auto_accept_member=True)
        lcom5 = LocalCommunity(name='lcom5', description='descl5', city='Paris', country='FR', gps_x=0, gps_y=0)
        tcom1 = TransportCommunity(name='tcom1', description='desct1', departure='dep1', arrival='arr1',
                                   auto_accept_member=True)
        tcom2 = TransportCommunity(name='tcom2', description='desct2', departure='dep2', arrival='arr2')
        tcom3 = TransportCommunity(name='tcom3', description='desct3', departure='dep3', arrival='arr3')
        tcom4 = TransportCommunity(name='tcom4', description='desct4', departure='dep4', arrival='arr4')
        tcom5 = TransportCommunity(name='tcom5', description='desct5', departure='dep4', arrival='arr5')
        lcom1.save()
        lcom2.save()
        lcom3.save()
        lcom4.save()
        lcom5.save()
        tcom1.save()
        tcom2.save()
        tcom3.save()
        tcom4.save()
        tcom5.save()

        own_mbr = Member(user=owner, community=lcom1, role='0', status='1')
        own_mbr.save()
        own_mbr = Member(user=owner, community=lcom2, role='0', status='1')
        own_mbr.save()

        own_mbr = Member(user=owner, community=lcom3, role='0', status='1')
        own_mbr.save()
        mod_mbr = Member(user=moderator, community=lcom3, role='1', status='0')
        mod_mbr.save()
        spl_mbr = Member(user=member, community=lcom3, role='2', status='0')
        spl_mbr.save()

        own_mbr = Member(user=owner, community=lcom4, role='0', status='1')
        own_mbr.save()
        mod_mbr = Member(user=moderator, community=lcom4, role='1', status='1')
        mod_mbr.save()
        spl_mbr = Member(user=member, community=lcom4, role='2', status='1')
        spl_mbr.save()

        own_mbr = Member(user=owner, community=lcom5, role='0', status='1')
        own_mbr.save()
        spl_mbr = Member(user=member, community=lcom5, role='2', status='2')
        spl_mbr.save()

        own_mbr = Member(user=owner, community=tcom1, role='0', status='1')
        own_mbr.save()
        own_mbr = Member(user=owner, community=tcom2, role='0', status='1')
        own_mbr.save()
        own_mbr = Member(user=owner, community=tcom3, role='0', status='1')
        own_mbr.save()
        own_mbr = Member(user=owner, community=tcom4, role='0', status='1')
        own_mbr.save()
        own_mbr = Member(user=owner, community=tcom5, role='0', status='1')
        own_mbr.save()

    def test_setup(self):
        self.assertEqual(4, User.objects.all().count())
        self.assertEqual(10, Community.objects.all().count())
        self.assertEqual(15, Member.objects.all().count())

    def test_join_wrong_community(self):
        """
        Ensure an authenticated user cannot join a community that does not exists
        """
        url = '/api/v1/communities/15/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user'))
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        self.assertEqual(15, Member.objects.all().count())

    def test_join_community_not_auto_accept(self):
        """
        Ensure an authenticated user can join a community
        """
        url = '/api/v1/communities/1/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user'))
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(16, Member.objects.all().count())
        member = Member.objects.get(user=User.objects.get(username='user'))
        community = Community.objects.get(id=1)
        self.assertEqual(community, member.community)
        self.assertEqual("2", member.role)
        self.assertEqual("0", member.status)

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(16, Member.objects.all().count())

    def test_join_community_auto_accept(self):
        """
        Ensure an authenticated user can join a community
        """
        url = '/api/v1/communities/2/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('user'))
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(16, Member.objects.all().count())
        member = Member.objects.get(user=User.objects.get(username='user'))
        community = Community.objects.get(id=2)
        self.assertEqual(community, member.community)
        self.assertEqual("2", member.role)
        self.assertEqual("1", member.status)

    def test_leave_community(self):
        """
        Ensure a member can leave a community
        """
        url = '/api/v1/communities/3/leave_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('member'))
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

        self.assertEqual(14, Member.objects.all().count())

    def test_leave_community_banned(self):
        """
        Ensure a banned member cannot leave a community
        """
        url = '/api/v1/communities/5/leave_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth('member'))
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.assertEqual(15, Member.objects.all().count())

    def test_list_my_memberships_without_auth(self):
        """
        Ensure an unauthenticated user cannot list memberships
        """
        url = '/api/v1/communities/0/list_my_memberships/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_my_memberships_member(self):
        """
        Ensure a user can list all his memberships
        """
        url = '/api/v1/communities/0/list_my_memberships/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('member'))
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

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('moderator'))
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

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('owner'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(10, data['count'])

    def test_list_members_without_auth(self):
        """
        Ensure non authenticated user cannot list community members
        """
        url = '/api/v1/communities/3/retrieve_members/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_members_without_member_rights(self):
        """
        Ensure a non-member authenticated user cannot list community members
        """
        url = '/api/v1/communities/3/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('user'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_without_mod_rights(self):
        """
        Ensure a simple user cannot list community members
        """
        url = '/api/v1/communities/3/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('member'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_with_mod_rights_not_accepted(self):
        """
        Ensure a moderator can list community members
        """
        url = '/api/v1/communities/3/retrieve_members/'

        # Test before acceptation
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('moderator'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_with_mod_rights(self):
        """
        Ensure a moderator can list community members
        """
        url = '/api/v1/communities/4/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('moderator'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(3, data['count'])

        self.assertEqual(6, data['results'][0]['id'])
        self.assertEqual('owner', data['results'][0]['user']['username'])
        self.assertEqual(1, data['results'][0]['user']['id'])
        self.assertEqual('0', data['results'][0]['role'])
        self.assertEqual('1', data['results'][0]['status'])

        self.assertEqual(7, data['results'][1]['id'])
        self.assertEqual('moderator', data['results'][1]['user']['username'])
        self.assertEqual(2, data['results'][1]['user']['id'])
        self.assertEqual('1', data['results'][1]['role'])
        self.assertEqual('1', data['results'][1]['status'])

        self.assertEqual(8, data['results'][2]['id'])
        self.assertEqual('member', data['results'][2]['user']['username'])
        self.assertEqual(3, data['results'][2]['user']['id'])
        self.assertEqual('2', data['results'][2]['role'])
        self.assertEqual('1', data['results'][2]['status'])

    def test_list_members_with_owner_rights(self):
        """
        Ensure an owner can list community members
        """
        url = '/api/v1/communities/4/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth('owner'))
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
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_accept_member_with_simple_member(self):
        """
        Ensure a simple member cannot accept members
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_accept_member_with_owner(self):
        """
        Ensure an owner can accept members
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('owner'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(5, data['id'])
        self.assertEqual('1', data['status'])
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

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('owner'), format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_accept_member_with_owner_not_found(self):
        """
        Ensure member exists
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 19
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('owner'), format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_accept_member_with_not_accepted_moderator(self):
        """
        Ensure an non accepted moderator cannot accept members
        """
        url = '/api/v1/communities/3/accept_member/'
        data = {
            'id': 5
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
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

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(5, data['id'])
        self.assertEqual('1', data['status'])
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
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ban_member_with_non_member(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_moderator_with_member(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 7
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_owner_with_member(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 6
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('member'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_member_with_moderator(self):
        """

        """
        url = '/api/v1/communities/4/ban_member/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(8, data['id'])
        self.assertEqual('2', data['status'])
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

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('owner'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(8, data['id'])
        self.assertEqual('2', data['status'])
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

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_without_auth(self):
        """

        """
        url = '/api/v1/communities/4/promote_moderator/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_promote_user_with_user(self):
        """

        """
        url = '/api/v1/communities/4/promote_moderator/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('user'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_with_moderator(self):
        """

        """
        url = '/api/v1/communities/4/promote_moderator/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('moderator'), format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_with_owner(self):
        """

        """
        url = '/api/v1/communities/4/promote_moderator/'
        data = {
            'id': 8
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth('owner'), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        data = response.data
        self.assertEqual(8, data['id'])
        self.assertEqual('1', data['role'])
