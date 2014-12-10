from django.contrib.auth.models import User
from django.db import models
from core.models import Skill
from core.models.reportable_model import ReportableModel
from core.models.request import Request


class Offer(ReportableModel):

    request = models.ForeignKey(Request)

    user = models.ForeignKey(User)

    skill = models.ForeignKey(Skill, blank=True, null=True)

    detail = models.TextField()

    closed = models.BooleanField(default=False)

    usefull = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request.title + ' - ' + self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'offer'
        verbose_name_plural = 'offers'
        app_label = 'core'
