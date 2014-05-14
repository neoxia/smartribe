from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):

    user = models.ForeignKey(User)

    description = models.TextField()

    class Meta:
        verbose_name = 'skill'
        verbose_name_plural = 'skills'
        app_label = 'core'