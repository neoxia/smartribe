from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


class Donation(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    amount = models.IntegerField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('donation')
        verbose_name_plural = _('donations')
        app_label = 'core'