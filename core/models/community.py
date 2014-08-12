from django.db import models
from core.models import Address


class Community(models.Model):

    name = models.CharField(max_length=50,
                            unique=True)

    description = models.TextField(max_length=180)

    banner = models.ImageField(blank=True,
                               null=True)

    logo = models.ImageField(blank=True,
                             null=True)

    creation_date = models.DateField(auto_now_add=True)

    last_update = models.DateField(auto_now=True)

    auto_accept_member = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'community'
        verbose_name_plural = 'communities'
        app_label = 'core'


class TransportStop(models.Model):

    name = models.CharField(max_length=50)

    detail = models.TextField(max_length=180,
                              null=True,
                              blank=True)

    #community = models.ForeignKey(TransportCommunity)

    #is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'transport stop'
        verbose_name_plural = 'transport stops'
        app_label = 'core'


class TransportCommunity(Community):

    departure = models.CharField(max_length=255)

    via = models.CharField(max_length=255,
                           null=True,
                           blank=True)

    arrival = models.CharField(max_length=255)

    #transport_stop_departure = models.ForeignKey(TransportStop, related_name='departure')
    #transport_stop_via = models.ForeignKey(TransportStop, related_name='via')
    #transport_stop_arrival = models.ForeignKey(TransportStop, related_name='arrival')

    def __str__(self):
        return self.name+', de '+self.departure \
               + 'à '+self.arrival \
               + ', via '+self.via

    class Meta:
        verbose_name = 'transport community'
        verbose_name_plural = 'transport communities'
        app_label = 'core'


class LocalCommunity(Community):

    address = models.ForeignKey(Address)

    class Meta:
        verbose_name = 'local community'
        verbose_name_plural = 'local communities'
        app_label = 'core'
