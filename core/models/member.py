from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models
from core.models.community import Community


class Member(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    community = models.ForeignKey(Community)

    ROLE_CHOICES = (
        ("0", _('Owner')),
        ("1", _('Moderator')),
        ("2", _('Member')),
    )
    role = models.CharField(max_length=10,
                            choices=ROLE_CHOICES,
                            default="2")

    STATUS_CHOICES = (
        ("0", _('Pending')),
        ("1", _('Accepted')),
        ("2", _('Banned')),
    )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default="0")

    registration_date = models.DateField(auto_now_add=True)

    last_modification_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.email + " / " + self.community.name + " / " + self.get_role_display() + " / " + \
               self.get_status_display()

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
        app_label = 'core'
