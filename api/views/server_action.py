import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from core.models import Request


class ServerActionViewSet(viewsets.ViewSet):
    """

    """

    @action(methods=['POST'])
    def auto_close_requests(self):
        """

        """
        requests = Request.objects.filter(auto_close=True, closed=False, expected_end_date__lt=datetime.date.today())
        for r in requests:
            r.closed = True
            r.end_date = datetime.date.today()
            r.save()