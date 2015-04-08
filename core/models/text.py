from django.utils.translation import ugettext as _
from django.db import models


class Text(models.Model):

    tag = models.CharField(max_length=255, unique=True)

    content = models.TextField()

    private = models.BooleanField(default=False)

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')
        app_label = 'core'
