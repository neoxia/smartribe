from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models
from core.models.skill import Skill
from core.models.reportable_model import ReportableModel
from core.models.request import Request


class Offer(ReportableModel):

    request = models.ForeignKey(Request)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    skill = models.ForeignKey(Skill, blank=True, null=True)

    detail = models.TextField()

    closed = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def get_photo(self):
        """ """
        from core.models.profile import Profile
        if Profile.objects.filter(user=self.user).exists():
            profile = Profile.objects.get(user=self.user)
            if profile.photo:
                return profile.photo.url[len(settings.MEDIA_URL):]
        return ''

    def get_skill_title(self):
        """ """
        if self.skill:
            return self.skill.title
        return ''

    def get_skill_description(self):
        """ """
        if self.skill:
            return self.skill.description
        return ''

    def is_evaluated(self):
        from core.models.evaluation import Evaluation
        return Evaluation.objects.filter(offer=self).exists()

    def __desc_str__(self):
        return self.user.email + " (" + self.request.__desc_str__() + ")"

    def __str__(self):
        return str(self.id) + " : " + self.__desc_str__()

    class Meta:
        verbose_name = _('offer')
        verbose_name_plural = _('offers')
        app_label = 'core'
