from django.utils.translation import ugettext as _
from django.db import models


class FaqSection(models.Model):

    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('FAQ section')
        verbose_name_plural = _('FAQ sections')
        app_label = 'core'
