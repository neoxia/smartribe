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
            if num % 2 == 0:
                aam = 0

            data = {
                'name': 'com'+num.__str__(),
                'description': 'com_desc'+num.__str__(),
                'auto_accept_member': aam,
            }
            self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')

    def set_create_community_with_member_na_and_moderator(self):
        self.set_create_community()
        # Set 1 simple user
        user = User.objects.get(username="simple_user")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)

        # Set 1 moderator
        user = User.objects.get(username="moderator")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        m = Member.objects.get(user=user)
        m.status = '1'
        m.role = '1'
        m.save()

    def set_create_community_with_member_and_moderator(self):
        self.set_create_community()
        # Set 1 simple user
        user = User.objects.get(username="simple_user")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        u = Member.objects.get(user=user)
        u.status = '1'
        u.save()

        # Set 1 moderator
        user = User.objects.get(username="moderator")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        m = Member.objects.get(user=user)
        m.status = '1'
        m.role = '1'
        m.save()

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
        self.assertEqual(4, data['count'])
        root_url = 'http://testserver'
        self.assertEqual(root_url+'/api/v1/communities/1/', data['results'][0]['community']['url'])
        self.assertEqual(root_url+'/api/v1/communities/3/', data['results'][1]['community']['url'])
        self.assertEqual(root_url+'/api/v1/communities/8/', data['results'][2]['community']['url'])
        self.assertEqual(root_url+'/api/v1/communities/9/', data['results'][3]['community']['url'])
        self.assertEqual('1', data['results'][0]['status'])
        self.assertEqual('1', data['results'][1]['status'])
        self.assertEqual('0', data['results'][2]['status'])
        self.assertEqual('1', data['results'][3]['status'])
        self.assertEqual('2', data['results'][0]['role'])
        self.assertEqual('1', data['results'][1]['role'])
        self.assertEqual('2', data['results'][2]['role'])
        self.assertEqual('2', data['results'][3]['role'])

        owner = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(owner)
        auth = 'JWT {0}'.format(token)

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(9, data['count'])

    def test_list_members_without_auth(self):
        """
        Ensure non authenticated user cannot list community members
        """
        self.set_create_communities_auto()

        url = '/api/v1/communities/1/retrieve_members/'

        response = self.client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_list_members_without_member_rights(self):
        """
        Ensure a non-member authenticated user cannot list community members
        """
        self.set_create_communities_auto()
        s_user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(s_user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_without_mod_rights(self):
        """
        Ensure a simple user cannot list community members
        """
        self.set_create_communities_auto()
        s_user = User.objects.get(username="simple_user")
        token = core.utils.gen_auth_token(s_user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)

        url = '/api/v1/communities/1/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_list_members_with_mod_rights(self):
        """
        Ensure a moderator can list community members
        """
        self.set_create_community()
        m_user = User.objects.get(username="moderator")
        token = core.utils.gen_auth_token(m_user)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/join_community/'
        self.client.post(url, HTTP_AUTHORIZATION=auth)
        m = Member.objects.get(id=2)
        m.role = '1'
        m.save()

        url = '/api/v1/communities/1/retrieve_members/'

        # Test before acceptation
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        m.status = '1'
        m.save()
        # Test after acceptation
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['count'])
        self.assertEqual(1, data['results'][0]['id'])
        self.assertEqual('community_owner', data['results'][0]['user']['username'])
        self.assertEqual('http://testserver/api/v1/users/1/', data['results'][0]['user']['url'])
        self.assertEqual(1, data['results'][0]['user']['id'])
        self.assertEqual('0', data['results'][0]['role'])
        self.assertEqual('1', data['results'][0]['status'])
        self.assertEqual(2, data['results'][1]['id'])
        self.assertEqual('moderator', data['results'][1]['user']['username'])
        self.assertEqual('http://testserver/api/v1/users/2/', data['results'][1]['user']['url'])
        self.assertEqual(2, data['results'][1]['user']['id'])
        self.assertEqual('1', data['results'][1]['role'])
        self.assertEqual('1', data['results'][1]['status'])

    def test_list_members_with_owner_rights(self):
        """
        Ensure an owner can list community members
        """
        self.set_create_community()
        owner = User.objects.get(username="community_owner")
        token = core.utils.gen_auth_token(owner)
        auth = 'JWT {0}'.format(token)

        url = '/api/v1/communities/1/retrieve_members/'

        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(1, data['count'])

    def test_accept_member_without_auth(self):
        """
        Ensure a non authenticated user can not accept members
        """
        self.set_create_community_with_member_na_and_moderator()

        url = '/api/v1/communities/1/accept_member/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_accept_member_with_simple_member(self):
        """
        Ensure a simple member cannot accept members
        """
        self.set_create_community_with_member_na_and_moderator()

        user = User.objects.get(username="simple_user")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/accept_member/'
        r_data = {
            'id': 2
        }

        response = self.client.post(url, r_data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_accept_member_with_owner(self):
        """
        Ensure an owner can accept members
        """
        self.set_create_community_with_member_na_and_moderator()

        user = User.objects.get(username="community_owner")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/accept_member/'
        r_data = {
            'id': 2
        }

        response = self.client.post(url, r_data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['id'])
        self.assertEqual('1', data['status'])

    def test_accept_member_with_owner_bad_request(self):
        """
        Ensure accept_member request data format
        """
        self.set_create_community_with_member_na_and_moderator()

        user = User.objects.get(username="community_owner")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/accept_member/'
        r_data = {
            'lol': 2
        }

        response = self.client.post(url, r_data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_accept_member_with_owner_not_found(self):
        """
        Ensure member exists
        """
        self.set_create_community_with_member_na_and_moderator()

        user = User.objects.get(username="community_owner")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/accept_member/'
        r_data = {
            'id': 14
        }

        response = self.client.post(url, r_data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_accept_member_with_moderator(self):
        """
        Ensure an owner can accept members
        """
        self.set_create_community_with_member_na_and_moderator()

        user = User.objects.get(username="moderator")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))
        url = '/api/v1/communities/1/accept_member/'
        r_data = {
            'id': 2
        }

        response = self.client.post(url, r_data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['id'])
        self.assertEqual('1', data['status'])

    def test_ban_member_without_auth(self):
        """

        """
        self.set_create_community_with_member_and_moderator()

        url = '/api/v1/communities/1/ban_member/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_ban_member_with_member(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="simple_user")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/ban_member/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_moderator_with_member(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="simple_user")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/ban_member/'
        data = {
            'id': 3
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_owner_with_member(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="simple_user")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/ban_member/'
        data = {
            'id': 1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_ban_member_with_moderator(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="moderator")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/ban_member/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['id'])
        self.assertEqual('2', data['status'])

    def test_ban_member_with_owner(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="community_owner")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/ban_member/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['id'])
        self.assertEqual('2', data['status'])

    def test_ban_owner_with_moderator(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="moderator")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/ban_member/'
        data = {
            'id': 1
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_without_auth(self):
        """

        """
        self.set_create_community_with_member_and_moderator()

        url = '/api/v1/communities/1/promote_moderator/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_promote_user_with_user(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="simple_user")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/promote_moderator/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_with_moderator(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="moderator")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/promote_moderator/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_promote_user_with_owner(self):
        """

        """
        self.set_create_community_with_member_and_moderator()
        user = User.objects.get(username="community_owner")
        auth = 'JWT {0}'.format(core.utils.gen_auth_token(user))

        url = '/api/v1/communities/1/promote_moderator/'
        data = {
            'id': 2
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.data
        self.assertEqual(2, data['id'])
        self.assertEqual('1', data['role'])
