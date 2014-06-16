from django.db import models
from django.contrib.auth.models import User
from core.models import Community


class Member(models.Model):

    user = models.ForeignKey(User)

    community = models.ForeignKey(Community)

    STATUS_CHOICES = (
                     ("0", 'Owner'),
                     ("1", 'Moderator'),
                     ("2", 'Member'),
    )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default="2")

    registration_date = models.DateField(auto_created=True)

    last_modification_date = models.DateField(auto_now=True)
