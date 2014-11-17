from django.db import models
from core.models.community import Community
from core.models.validator import ZipCodeValidatorFR


class LocalCommunity(Community):

    gps_x = models.FloatField()

    gps_y = models.FloatField()

    street_num = models.IntegerField(blank=True, null=True)

    street = models.CharField(max_length=100,
                              blank=True, null=True)

    zip_code = models.CharField(max_length=10,
                                blank=True, null=True,
                                validators=[ZipCodeValidatorFR(), ])

    city = models.CharField(max_length=100)

    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'local community'
        verbose_name_plural = 'local communities'
        app_label = 'core'
