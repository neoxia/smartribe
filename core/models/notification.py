from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):

    photo = models.ImageField(null=True, blank=True)

    user = models.ForeignKey(User)

    title = models.CharField(max_length=255)

    message = models.CharField(max_length=255)

    link = models.CharField(max_length=255)

    seen = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        app_label = 'core'
