import os
from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models
from core.models.validator import PhoneValidatorFR, ZipCodeValidatorFR


def get_photo_path(self, filename):
    _, ext = os.path.splitext(filename)
    url = "profiles/%s/picture%s" % (str(self.user.id), ext)
    return url

#fs = FileSystemStorage(location='/media/photos')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')

    GENDER_CHOICES = (
                     ('M', _('Male')),
                     ('F', _('Female')),
                     ('O', _('Other')),
    )
    gender = models.CharField(max_length=2,
                              choices=GENDER_CHOICES,
                              default='O')

    street_num = models.IntegerField(blank=True, null=True)

    street = models.CharField(max_length=100,
                              blank=True, null=True)

    zip_code = models.CharField(max_length=10,
                                blank=True, null=True,
                                validators=[ZipCodeValidatorFR(), ])

    city = models.CharField(max_length=100,
                            blank=True, null=True)

    country = models.CharField(max_length=50,
                               blank=True, null=True)

    phone = models.CharField(max_length=15,
                             validators=[PhoneValidatorFR(), ],
                             blank=True,
                             null=True)

    birthdate = models.DateField(blank=True,
                                 null=True)

    bio = models.TextField(blank=True,
                           null=True)

    photo = models.ImageField(upload_to=get_photo_path,
                              #storage=fs,
                              blank=True,
                              null=True)

    mail_notification = models.BooleanField(default=True)

    CONTACT_CHOICES = (
        ('E', _('Email')),
        ('P', _('Phone')),
        ('N', _('None')))
    favorite_contact = models.CharField(max_length=2,
                                        choices=CONTACT_CHOICES,
                                        default='N')

    def get_skills(self):
        # TODO : Test
        from core.models.skill import Skill
        return Skill.objects.filter(user=self.user)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        app_label = 'core'


