from core.models.user import User
from django.db import models


class ActivationToken(models.Model):

    user = models.ForeignKey(User)

    token = models.CharField(max_length=64)

    request_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'activation token'
        verbose_name_plural = 'activation tokens'
        app_label = 'core'
