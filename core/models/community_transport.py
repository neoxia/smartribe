from django.db import models
from core.models.community import Community


class TransportCommunity(Community):

    departure = models.CharField(max_length=255)

    via = models.CharField(max_length=255,
                           null=True, blank=True)

    arrival = models.CharField(max_length=255)

    def __str__(self):
        return self.name+', de '+self.departure \
            + ' à '+self.arrival \
            + ', via '+self.via

    class Meta:
        verbose_name = 'transport community'
        verbose_name_plural = 'transport communities'
        app_label = 'core'
