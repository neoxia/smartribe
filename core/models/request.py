from django.contrib.auth.models import User
from django.db import models
from core.models.reportable_model import ReportableModel
from core.models.skill import SkillCategory


class Request(ReportableModel):

    user = models.ForeignKey(User)

    category = models.ForeignKey(SkillCategory)

    title = models.CharField(max_length=255)

    detail = models.TextField()

    creation_date = models.DateField(auto_now_add=True)

    expected_end_date = models.DateField(blank=True,
                                         null=True)

    end_date = models.DateField(blank=True,
                                null=True)

    auto_close = models.BooleanField(default=False)

    closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'request'
        verbose_name_plural = 'requests'
        app_label = 'core'
