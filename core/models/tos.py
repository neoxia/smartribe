from django.utils.translation import ugettext as _
from django.db import models


class Tos(models.Model):
    version = models.CharField(max_length=50)

    date = models.DateField()

    terms = models.TextField()

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = _('tos')
        verbose_name_plural = _('tos')
        app_label = 'core'
