import os
from django.utils.translation import ugettext as _
from django.db import models


def get_banner_path(self, filename):
    _, ext = os.path.splitext(filename)
    url = "communities/%s/banner/banner.%s" % (str(self.id), ext)
    return url


def get_logo_path(self, filename):
    _, ext = os.path.splitext(filename)
    url = "communities/%s/logo/%s" % (str(self.id), ext)
    return url


class Community(models.Model):

    name = models.CharField(max_length=50, unique=True)

    description = models.TextField()

    banner = models.ImageField(upload_to=get_banner_path,
                               blank=True, null=True)

    logo = models.ImageField(upload_to=get_logo_path,
                             blank=True, null=True)

    creation_date = models.DateField(auto_now_add=True)

    last_update = models.DateField(auto_now=True)

    auto_accept_member = models.BooleanField(default=False)

    def get_type(self):
        """
        Returns the type of the community as a capital letter.
        """
        from core.models.community_local import LocalCommunity
        from core.models.community_transport import TransportCommunity
        try:
            self.localcommunity
            return "L"
        except LocalCommunity.DoesNotExist:
            pass
        try:
            self.transportcommunity
            return "T"
        except TransportCommunity.DoesNotExist:
            pass
        return "O"

    def get_members_count(self):
        from core.models.member import Member
        return Member.objects.filter(community=self, status='1').count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('community')
        verbose_name_plural = _('communities')
        app_label = 'core'



