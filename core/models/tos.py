from django.db import models

class Tos(models.Model):
    version = models.CharField(max_length=50)

    date = models.DateField()

    terms = models.TextField()

    def __str__(self):
        return self.version

    class Meta:
        verbose_name = 'tos'
        verbose_name_plural = 'tos'
        app_label = 'core'