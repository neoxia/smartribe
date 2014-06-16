from django.db import models
from django.contrib.auth.models import User
from core.models import Community


class Member(models.Model):

    user = models.ForeignKey(User)

    community = models.ForeignKey(Community)

    ROLE_CHOICES = (
                     ("0", 'Owner'),
                     ("1", 'Moderator'),
                     ("2", 'Member'),
    )
    role = models.CharField(max_length=10,
                              choices=ROLE_CHOICES,
                              default="2")

    STATUS_CHOICES = (
                     ("0", 'Pending'),
                     ("1", 'Accepted'),
                     ("2", 'Banned'),
    )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default="0")

    registration_date = models.DateField(auto_now_add=True)

    last_modification_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'
        app_label = 'core'
