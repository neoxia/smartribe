from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from core.models.offer import Offer
from core.models.reportable_model import ReportableModel


class Message(ReportableModel):

    offer = models.ForeignKey(Offer)

    user = models.ForeignKey(User)

    content = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    def get_photo(self):
        """ """
        from core.models.profile import Profile
        if Profile.objects.filter(user=self.user).exists():
            profile = Profile.objects.get(user=self.user)
            if profile.photo:
                return profile.photo.url[len(settings.MEDIA_URL):]
        return ''

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' - Offer : ' + str(self.offer.id)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        app_label = 'core'
