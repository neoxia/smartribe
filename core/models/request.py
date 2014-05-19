from django.db import models
from django.contrib.auth.models import User

__author__ = 'Renaud'

class Request(models.Model):

    user = models.ForeignKey(User)

    title = models.CharField(max_length=50)

    description = models.TextField()

    class Meta:
        verbose_name = 'request'
        verbose_name_plural = 'requests'
        app_label = 'core'
