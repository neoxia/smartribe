from django.contrib.auth.models import User
from django.db import models
from core.models import Offer
from core.models.location import MeetingPoint
from core.models.reportable_model import ReportableModel


class Meeting(models.Model):

    offer = models.ForeignKey(Offer)

    user = models.ForeignKey(User)

    meeting_point = models.ForeignKey(MeetingPoint)

    date_time = models.DateTimeField()

    STATUS_CHOICES = {
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Refused'),
    }
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default='P')

    is_validated = models.BooleanField(default=False)

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'meeting'
        verbose_name_plural = 'meetings'
        app_label = 'core'


class MeetingMessage(ReportableModel):

    meeting = models.ForeignKey(Meeting)

    user = models.ForeignKey(User)

    creation_date = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    class Meta:
        verbose_name = 'meeting message'
        verbose_name_plural = 'meeting messages'
        app_label = 'core'
