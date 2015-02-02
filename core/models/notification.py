from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):

    user = models.ForeignKey(User)

    message = models.CharField(max_length=255)

    link = models.TextField(max_length=255)

    seen = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        app_label = 'core'
