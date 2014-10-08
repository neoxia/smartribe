import datetime

from django.conf import settings

from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from core.models import Request
from core.models.password_recovery import PasswordRecovery


@api_view(['POST'])
@permission_classes((AllowAny,))
@throttle_classes([AnonRateThrottle])
def auto_close_requests(request):
    """

    """
    requests = Request.objects.filter(auto_close=True, closed=False, expected_end_date__lt=datetime.date.today())
    for r in requests:
        r.closed = True
        r.end_date = datetime.date.today()
        r.save()
    return Response(status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@throttle_classes([AnonRateThrottle])
def clean_password_recovery_tokens(request):
    """
    Delete automatically password recovery tokens which lifetime exceeds
    the PRT_VALIDITY setting.
    """
    #TODO : Test
    limit = datetime.datetime.now() - datetime.timedelta(hours = settings.PRT_VALIDITY)
    tokens = PasswordRecovery.objects.filter(request_datetime__lt=limit)
    for t in tokens:
        t.delete()
    return Response(status.HTTP_200_OK)


#TODO : Moderation : Analyse if more than five identical objects are reported.
