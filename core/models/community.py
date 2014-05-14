from django.db import models


class Community(models.Model):
    name = models.CharField(max_length=50)
    

    class Meta:
        verbose_name = 'community'
        verbose_name_plural = 'communities'
        app_label = 'core'
