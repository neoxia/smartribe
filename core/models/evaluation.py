from django.contrib.auth.models import User
from django.db import models
from core.models import Meeting
from core.models.reportable_model import ReportableModel


class Evaluation(ReportableModel):

    meeting = models.ForeignKey(Meeting)

    DANGEROUS = 0
    BAD = 1
    NEUTRAL = 2
    GOOD = 3
    EXCELLENT = 4
    PERFECT = 5
    EVALUATION_CHOICES = {
        (DANGEROUS, 'Dangerous'),
        (BAD, 'Bad'),
        (NEUTRAL, 'Neutral'),
        (GOOD, 'Good'),
        (EXCELLENT, 'Excellent'),
        (PERFECT, 'Perfect'),
    }
    mark = models.IntegerField(choices=EVALUATION_CHOICES)

    comment = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meeting.offer.user.username + ', ' + self.id.__str__()

    class Meta:
        verbose_name = 'evaluation'
        verbose_name_plural = 'evaluations'
        app_label = 'core'