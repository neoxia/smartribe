from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models


class Inappropriate(models.Model):

    user = models.ForeignKey(User)

    content_identifier = models.CharField(max_length=255)

    detail = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content_identifier

    class Meta:
        verbose_name = _('inappropriate content')
        verbose_name_plural = _('inappropriate contents')
        app_label = 'core'

