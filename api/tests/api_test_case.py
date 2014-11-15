from django.contrib.auth.models import User
from rest_framework.test import APITestCase
import core.utils


class CustomAPITestCase(APITestCase):

    def auth(self, username):
        user = User.objects.get(username=username)
        token = core.utils.gen_auth_token(user)
        return 'JWT {0}'.format(token)
