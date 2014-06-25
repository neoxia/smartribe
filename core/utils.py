from rest_framework_jwt import utils

def gen_auth_token(user=None):
    payload = utils.jwt_payload_handler(user)
    return utils.jwt_encode_handler(payload)
