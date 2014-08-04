from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Member, Community
import core.utils


class MemberTests(APITestCase):

    def setUp(self):
        """
        Make a user for authenticating and
        testing community actions
        """
        owner = User(username="community_owner", password="test", email="z@s.d")
        owner.save()
        moderator = User(username="moderator", password="test0", email="z@s.sd")
        moderator.save()
        user = User(username="simple_user", password="test1", email="zz@ssk.dk")
        user.save()

    def set_create_community(self):
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'name': 'com',
            'description': 'com_desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

    def set_create_community_auto(self):
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'name': 'com',
            'description': 'com_desc',
            'auto_accept_member': 1,
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

    def set_create_communities_auto(self):
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        for num in range(1, 10):
            url = '/api/v1/communities/'
            aam = 1
            if num%2 == 0:
                aam = 0

            data = {
                'name': 'com'+num.__str__(),
                'description': 'com_desc'+num.__str__(),
                'auto_accept_member': aam,
            }
            self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

    def test_join_wrong_community(self):
        """
        Ensure an authenticated user cannot join a community that does not exists
        """
        self.set_create_community()
        user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/2/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(1, Member.objects.all().count())

    def test_join_community_not_auto_accept(self):
        """
        Ensure an authenticated user can join a community
        """
        self.set_create_community()
        user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Member.objects.all().count())
        member = Member.objects.get(user=user)
        community = Community.objects.get(id=1)
        self.assertEqual(community, member.community)
        self.assertEqual("2", member.role)
        self.assertEqual("0", member.status)

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, Member.objects.all().count())

    def test_join_community_auto_accept(self):
        """
        Ensure an authenticated user can join a community
        """
        self.set_create_community_auto()
        user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/join_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Member.objects.all().count())
        member = Member.objects.get(user=user)
        community = Community.objects.get(id=1)
        self.assertEqual(community, member.community)
        self.assertEqual("2", member.role)
        self.assertEqual("1", member.status)

    def test_leave_community(self):
        """
        Ensure a member can leave a community
        """
        self.set_create_community()
        user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)

        url = '/api/v1/communities/1/leave_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Member.objects.all().count())

    def test_leave_community_banned(self):
        """
        Ensure a banned member cannot leave a community
        """
        self.set_create_community()
        user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)

        member = Member.objects.get(user=user)
        member.status = '2'
        member.save()

        url = '/api/v1/communities/1/leave_community/'

        response = self.client.post(url, HTTP_AUTHORIZATION=auth)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, Member.objects.all().count())

    def test_list_my_memberships_without_auth(self):
        """
        Ensure an unauthenticated user cannot list memberships
        """
        url = '/api/v1/communities/0/list_my_memberships/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_my_memberships(self):
        """
        Ensure a user can list all his memberships
        """
        self.set_create_communities_auto()
        self.assertEqual(9, Community.objects.all().count())
        s_user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(s_user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        url = '/api/v1/communities/3/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        m = Member.objects.get(id=11)
        m.role = '1'
        m.save()
        url = '/api/v1/communities/6/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        url = '/api/v1/communities/6/leave_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        url = '/api/v1/communities/8/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        url = '/api/v1/communities/9/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)

        url = '/api/v1/communities/0/list_my_memberships/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(4, len(data))
        self.assertEqual('/api/v1/communities/1/', data[0]['community']['url'])
        self.assertEqual('/api/v1/communities/3/', data[1]['community']['url'])
        self.assertEqual('/api/v1/communities/8/', data[2]['community']['url'])
        self.assertEqual('/api/v1/communities/9/', data[3]['community']['url'])
        self.assertEqual('1', data[0]['status'])
        self.assertEqual('1', data[1]['status'])
        self.assertEqual('0', data[2]['status'])
        self.assertEqual('1', data[3]['status'])
        self.assertEqual('2', data[0]['role'])
        self.assertEqual('1', data[1]['role'])
        self.assertEqual('2', data[2]['role'])
        self.assertEqual('2', data[3]['role'])

        owner = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(owner)
        auth = 'JWT {0}'.format(token)

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(9, len(data))
