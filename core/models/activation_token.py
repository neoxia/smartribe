from django.conf import settings
from django.utils.translation import ugettext as _
from django.db import models


class ActivationToken(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    token = models.CharField(max_length=64)

    request_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('activation token')
        verbose_name_plural = _('activation tokens')
        app_label = 'core'
