from django.contrib.auth.models import User
from django.db import models
from core.models import Meeting
from core.models.reportable_model import ReportableModel


class MeetingMessage(ReportableModel):

    meeting = models.ForeignKey(Meeting)

    user = models.ForeignKey(User)

    creation_date = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    class Meta:
        verbose_name = 'meeting message'
        verbose_name_plural = 'meeting messages'
        app_label = 'core'
