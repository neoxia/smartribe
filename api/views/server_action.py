import datetime

from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from core.models import Request


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


#TODO : Implement a method to limit validity of password recovery tokens


