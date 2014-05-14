from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    GENDER_CHOICES = (
                     ('M', 'Male'),
                     ('F', 'Female'),
                     ('O', 'Other'),
    )
    gender = models.CharField(max_length=2,
                              choices=GENDER_CHOICES,
                              default='O')

    birthdate = models.DateField()

    bio = models.TextField()

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        app_label = 'core'
