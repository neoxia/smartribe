from django.db import models
from django.contrib.auth.models import User
from core.models.validator import PhoneValidatorFR, ZipCodeValidatorFR

def get_photo(self, filename):
    url = "profiles/%s/%s" % (self.user.username, filename)
    return url

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    GENDER_CHOICES = (
                     ('M', 'Male'),
                     ('F', 'Female'),
                     ('O', 'Other'),
    )
    gender = models.CharField(max_length=2,
                              choices=GENDER_CHOICES,
                              default='O')

    phone = models.CharField(max_length=15,
                             validators=[PhoneValidatorFR(), ],
                             blank=True,
                             null=True)

    birthdate = models.DateField(blank=True,
                                 null=True)

    bio = models.TextField(blank=True,
                           null=True)

    photo = models.ImageField(upload_to=get_photo,
                              blank=True,
                              null=True)



    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        app_label = 'core'


class Address(models.Model):

    profile = models.OneToOneField(Profile,
                                   related_name='address')

    num = models.IntegerField()

    street = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    zip_code = models.CharField(max_length=10,
                                validators=[ZipCodeValidatorFR(), ])

    country = models.CharField(max_length=50)

    #objects = models.GeoManager()

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        app_label = 'core'