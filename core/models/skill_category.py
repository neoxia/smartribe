from django.db import models


class SkillCategory(models.Model):

    name = models.CharField(max_length=50)

    detail = models.TextField()

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'skill category'
        verbose_name_plural = 'skill categories'
        app_label = 'core'
