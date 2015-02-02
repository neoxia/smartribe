from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models


class PasswordRecovery(models.Model):

    user = models.ForeignKey(User)

    token = models.CharField(max_length=64)

    ip_address = models.IPAddressField()

    request_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('password recovery')
        verbose_name_plural = _('password recoveries')
        app_label = 'core'
