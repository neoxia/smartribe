from django.db import models
from core.models.request import Request

__author__ = 'Renaud'

class Offer(models.Model):

    request = models.ForeignKey(Request)

    description = models.TextField()

    class Meta:
        verbose_name = 'offer'
        verbose_name_plural = 'offers'
        app_label = 'core'