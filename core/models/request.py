from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from core.models.community import Community
from core.models.reportable_model import ReportableModel
from core.models.skill import SkillCategory


class Request(ReportableModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

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
            profile = Profile.objects.get(user=self.user)
            if profile.photo:
                return profile.photo.url[len(settings.MEDIA_URL):]
        return ''

    def get_offers_count(self):
        """  """
        from core.models.offer import Offer
        return Offer.objects.filter(request=self).count()

    def __desc_str__(self):
        return self.user.email + " / " + self.category.name + " / " + self.title

    def __str__(self):
        return str(self.id) + " : " + self.__desc_str__()

    class Meta:
        verbose_name = _('request')
        verbose_name_plural = _('requests')
        app_label = 'core'
