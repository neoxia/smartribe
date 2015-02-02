from django.utils.translation import ugettext as _
from django.db import models
from core.models import FaqSection


class Faq(models.Model):

    section = models.ForeignKey(FaqSection)

    private = models.BooleanField(default=True)

    question = models.CharField(max_length=255)

    answer = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _('frequently asked question')
        verbose_name_plural = _('frequently asked questions')
        app_label = 'core'
