from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from core.models import Skill
from core.models.reportable_model import ReportableModel
from core.models.request import Request


class Offer(ReportableModel):

    request = models.ForeignKey(Request)

    user = models.ForeignKey(User)

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

    def get_skill_description(self):
        """ """
        if self.skill:
            return self.skill.description
        return ''

    def __str__(self):
        return self.request.title + ' - ' + self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'offer'
        verbose_name_plural = 'offers'
        app_label = 'core'
