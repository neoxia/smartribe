from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
import core.utils


class CustomAPITestCase(APITestCase):

    user_model = get_user_model()

    def auth(self, name):
        email = name + '@test.com'
        user = self.user_model.objects.get(email=email)
        token = core.utils.gen_auth_token(user)
        return 'JWT {0}'.format(token)
