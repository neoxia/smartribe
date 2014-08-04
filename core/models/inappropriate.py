from django.contrib.auth.models import User
from django.db import models


class Inappropriate(models.Model):

    user = models.ForeignKey(User)

    content_url = models.URLField()

    detail = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content_url

    class Meta:
        verbose_name = 'inappropriate content'
        verbose_name_plural = 'inappropriate contents'
        app_label = 'core'

