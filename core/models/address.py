from django.db import models
from core.models.validator import ZipCodeValidatorFR


class Address(models.Model):

    num = models.IntegerField(blank=True,
                              null=True)

    street = models.CharField(max_length=100,
                              blank=True,
                              null=True)

    city = models.CharField(max_length=100)

    zip_code = models.CharField(max_length=10,
                                validators=[ZipCodeValidatorFR(), ],
                                blank=True,
                                null=True)

    country = models.CharField(max_length=50)

    #objects = models.GeoManager()

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        app_label = 'core'
