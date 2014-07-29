from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User
from core.models import Member, Community
import core.utils


class CommunityTests(APITestCase):

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

    def create_community(self):
        user = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/'
        data = {
            'name': 'com',
            'description': 'com_desc',
        }
        self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

    def create_community_auto(self):
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

    def test_join_wrong_community(self):
        """
        Ensure an authenticated user cannot join a community that does not exists
        """
        self.create_community()
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
        self.create_community()
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
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, Member.objects.all().count())

    def test_join_community_auto_accept(self):
        """
        Ensure an authenticated user can join a community
        """
        self.create_community_auto()
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
        self.create_community()
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
        self.create_community()
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
