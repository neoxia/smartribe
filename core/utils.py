import random
import string
from rest_framework_jwt import utils

def gen_auth_token(user=None):
    payload = utils.jwt_payload_handler(user)
    return utils.jwt_encode_handler(payload)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def gen_pwd_recovery_token(size=64, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))