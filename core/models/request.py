from django.contrib.auth.models import User
from django.db import models
from core.models import Community
from core.models.reportable_model import ReportableModel
from core.models.skill import SkillCategory


class Request(ReportableModel):

    user = models.ForeignKey(User)

    community = models.ForeignKey(Community, blank=True, null=True)

    category = models.ForeignKey(SkillCategory)

    title = models.CharField(max_length=255)

    detail = models.TextField()

    created_on = models.DateField(auto_now_add=True)

    expected_end_date = models.DateField(blank=True,
                                         null=True)

    end_date = models.DateField(blank=True,
                                null=True)

    auto_close = models.BooleanField(default=False)

    closed = models.BooleanField(default=False)

    last_update = models.DateTimeField(auto_now=True)

    def get_photo(self):
        """ """
        from core.models.profile import Profile
        if Profile.objects.filter(user=self.user).exists():
            return Profile.objects.get(user=self.user).photo
        return ''

    def get_offers_count(self):
        """  """
        from core.models.offer import Offer
        return Offer.objects.filter(request=self).count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'request'
        verbose_name_plural = 'requests'
        app_label = 'core'
