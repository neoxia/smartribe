from django.contrib.auth.models import User
from django.db import models
from core.models.offer import Offer
from core.models.reportable_model import ReportableModel


class Message(ReportableModel):

    offer = models.ForeignKey(Offer)

    user = models.ForeignKey(User)

    content = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        app_label = 'core'
