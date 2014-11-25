from django.contrib.auth.models import User
from django.db import models
from core.models.offer import Offer
from core.models.reportable_model import ReportableModel


class MeetingMessage(ReportableModel):

    offer = models.ForeignKey(Offer)

    user = models.ForeignKey(User)

    content = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'meeting message'
        verbose_name_plural = 'meeting messages'
        app_label = 'core'
