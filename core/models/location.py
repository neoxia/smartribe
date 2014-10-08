from django.db import models
from core.models import Community


def get_photo_path(self, filename):
    url = "meeting_points/%s/%s" % (self.id.__str__, filename)
    return url


class Location(models.Model):

    #TODO : Add creator

    community = models.ForeignKey(Community)

    name = models.CharField(max_length=50)

    description = models.TextField()

    index = models.IntegerField(null=True, blank=True)

    gps_x = models.FloatField()

    gps_y = models.FloatField()

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'locations'
        app_label = 'core'


class MeetingPoint(models.Model):

    location = models.ForeignKey(Location)

    name = models.CharField(max_length=50)

    description = models.TextField()

    photo = models.ImageField(upload_to=get_photo_path,
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = 'meeting point'
        verbose_name_plural = 'meeting points'
        app_label = 'core'


