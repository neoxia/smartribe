import os
from django.utils.translation import ugettext as _
from django.db import models
from core.models.location import Location


def get_photo_path(self, filename):
    _, ext = os.path.splitext(filename)
    url = "meeting_points/%s/photo%s" % (str(self.id), ext)
    return url


class MeetingPoint(models.Model):

    location = models.ForeignKey(Location)

    name = models.CharField(max_length=50)

    description = models.TextField(null=True, blank=True)

    photo = models.ImageField(upload_to=get_photo_path,
                              blank=True,
                              null=True)

    def __desc_str__(self):
        return self.name

    def __str__(self):
        return str(self.id) + ' : ' + self.location.__desc_str__() + " / " + self.__desc_str__()

    class Meta:
        verbose_name = _('meeting point')
        verbose_name_plural = _('meeting points')
        app_label = 'core'
