from django.contrib.auth.models import User
from django.db import models
from core.models.community import Community


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

    def __str__(self):
        return self.user.username + " / " + self.community.name + " / " + self.get_role_display() + " / " + \
               self.get_status_display()

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'
        app_label = 'core'
