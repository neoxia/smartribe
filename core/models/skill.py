from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from core.models.skill_category import SkillCategory


class Skill(models.Model):

    user = models.ForeignKey(User)

    category = models.ForeignKey(SkillCategory)

    description = models.TextField()

    MEDIUM = 1
    HIGH = 2
    EXPERT = 3
    LEVEL_CHOICES = (
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (EXPERT, 'Expert')
    )
    level = models.IntegerField(default=MEDIUM,
                                choices=LEVEL_CHOICES)

    def get_average_mark(self):
        from core.models.evaluation import Evaluation
        return Evaluation.objects.filter(offer__skill=self).aggregate(average_eval=Avg('mark'))['average_eval']

    def get_mark_count(self):
        # TODO : Test
        from core.models.evaluation import Evaluation
        return Evaluation.objects.filter(offer__skill=self).count()

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'skill'
        verbose_name_plural = 'skills'
        app_label = 'core'
