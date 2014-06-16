from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    name = models.CharField(max_length=50)

    description = models.TextField()

    creator = models.ForeignKey(User)

    banner = models.ImageField(blank=True,
                               null=True)

    logo = models.ImageField(blank=True,
                             null=True)

    creation_date = models.DateField(auto_created=True)

    auto_accept_member = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'community'
        verbose_name_plural = 'communities'
        app_label = 'core'
