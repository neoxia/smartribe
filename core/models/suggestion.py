from django.db import models
from django.contrib.auth.models import User


class Suggestion(models.Model):

    CATEGORY_CHOICES = (
        ('B', 'Bug report'),
        ('U', 'Upgrade'),
        ('O', 'Others'),
    )
    category = models.CharField(max_length=1,
                                choices=CATEGORY_CHOICES,
                                default='O')

    user = models.ForeignKey(User)

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True,
                                   null=True)

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'suggestion'
        verbose_name_plural = 'suggestions'
        app_label = 'core'
