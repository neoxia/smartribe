from django.contrib.auth.models import User
from django.db import models
from core.models.reportable_model import ReportableModel
from core.models.request import Request


class Offer(ReportableModel):

    request = models.ForeignKey(Request)

    user = models.ForeignKey(User)

    detail = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'offer'
        verbose_name_plural = 'offers'
        app_label = 'core'
