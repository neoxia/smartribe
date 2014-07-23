from core.models.user import User
from django.db import models
from core.models.request import Request


class Offer(models.Model):

    request = models.ForeignKey(Request)

    user = models.ForeignKey(User)

    detail = models.TextField()

    creation_date = models.TextField()

    class Meta:
        verbose_name = 'offer'
        verbose_name_plural = 'offers'
        app_label = 'core'
