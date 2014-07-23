from core.models.user import User
from django.db import models


class PasswordRecovery(models.Model):

    user = models.ForeignKey(User)

    token = models.CharField(max_length=64)

    ip_address = models.IPAddressField()

    request_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'password recovery'
        verbose_name_plural = 'password recoveries'
        app_label = 'core'
