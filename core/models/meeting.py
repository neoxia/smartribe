from django.contrib.auth.models import User
from django.db import models
from core.models import Offer
from core.models.location import MeetingPoint


class Meeting(models.Model):

    offer = models.ForeignKey(Offer)

    meeting_point = models.ForeignKey(MeetingPoint)

    date_time = models.DateTimeField()

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'meeting'
        verbose_name_plural = 'meetings'
        app_label = 'core'


class MeetingMessage(models.Model):

    meeting = models.ForeignKey(Meeting)

    user = models.ForeignKey(User)

    date_time = models.DateTimeField()

    content = models.TextField()

    class Meta:
        verbose_name = 'meeting message'
        verbose_name_plural = 'meeting messages'
        app_label = 'core'
