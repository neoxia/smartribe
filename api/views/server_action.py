import datetime

from django.conf import settings
from django.db.models import Count

from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from api.utils.asyncronous_mail import send_mail
from core.models import Request, Inappropriate
from core.models.password_recovery import PasswordRecovery
from smartribe.settings import INAP_LIMIT


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
    limit = datetime.datetime.now() - datetime.timedelta(hours=settings.PRT_VALIDITY)
    tokens = PasswordRecovery.objects.filter(request_datetime__lt=limit)
    for t in tokens:
        t.delete()
    return Response(status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
#@throttle_classes([AnonRateThrottle])
def manage_reported_objects(request):
    """
    Analyses if a single object is reported more than five time.
    If yes, it warns service administrators.
    """
    #TODO : Throttle
    qs = Inappropriate.objects.values('content_identifier').annotate(total=Count('content_identifier'))
    #qs = qs.order_by('content_identifier')
    for obj in qs:
        if obj['total'] > INAP_LIMIT:
            message = 'Content URL :\n' + obj['content_identifier'] \
                + '\n\nThis content has been reported as inappropriate more than ' + str(INAP_LIMIT) + ' times.' \
                + '\n\nPlease, specific attention required !'

            send_mail('[SmarTribe] Inappropriate content warning : ' + obj['content_identifier'],
                      message,
                      'noreply@smartribe.fr',
                      ['contact@smartribe.fr'])
    return Response(status.HTTP_200_OK)
