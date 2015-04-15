from django.conf import settings
from django.utils.translation import ugettext as _
from django.db import models
from django.db.models import Avg
from core.models.skill_category import SkillCategory


class Skill(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    category = models.ForeignKey(SkillCategory)

    title = models.CharField(max_length=32)

    description = models.TextField(null=True, blank=True)

    MEDIUM = 1
    HIGH = 2
    EXPERT = 3
    LEVEL_CHOICES = (
        (MEDIUM, _('Medium')),
        (HIGH, _('High')),
        (EXPERT, _('Expert'))
    )
    level = models.IntegerField(default=MEDIUM,
                                choices=LEVEL_CHOICES)

    def get_average_mark(self):
        from core.models.evaluation import Evaluation
        return Evaluation.objects.filter(offer__skill=self).aggregate(average_eval=Avg('mark'))['average_eval']

    def get_mark_count(self):
        from core.models.evaluation import Evaluation
        return Evaluation.objects.filter(offer__skill=self).count()

    def get_category_name(self):
        return self.category.name

    def __desc_str__(self):
        return self.user.email + " / " + self.category.name + " / " + self.get_level_display()

    def __str__(self):
        return str(self.id) + " : " + self.__desc_str__()

    class Meta:
        verbose_name = _('skill')
        verbose_name_plural = _('skills')
        app_label = 'core'
