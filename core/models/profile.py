from django.contrib.auth.models import User
from django.db import models
from core.models.address import Address
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

    address = models.OneToOneField(Address,
                                   related_name='profile',
                                   blank=True,
                                   null=True)

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

    CONTACT_CHOICES = (
        ('E', 'Email'),
        ('P', 'Phone'),
        ('N', 'None'))
    favorite_contact = models.CharField(max_length=2,
                                        choices=CONTACT_CHOICES,
                                        default='N')
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        app_label = 'core'


