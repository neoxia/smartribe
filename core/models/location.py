from django.db import models
from core.models import Community


class Location(models.Model):

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

    name = models.CharField(max_length=50)

    description = models.TextField()

    photo = models.ImageField()

    class Meta:
        verbose_name = 'meeting point'
        verbose_name_plural = 'meeting points'
        app_label = 'core'


