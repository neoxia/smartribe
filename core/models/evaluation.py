from django.contrib.auth.models import User
from django.db import models
from core.models import Meeting


class Evaluation(models.Model):

    meeting = models.ForeignKey(Meeting)

    EVALUATION_CHOICES = {
        ('0', 'Dangerous'),
        ('1', 'Bad'),
        ('2', 'Neutral'),
        ('3', 'Good'),
        ('4', 'Excellent'),
        ('5', 'Perfect'),
    }
    mark = models.CharField(max_length=1,
                            choices=EVALUATION_CHOICES)

    comment = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meeting.offer.user.username + ', ' + self.id.__str__()

    class Meta:
        verbose_name = 'evaluation'
        verbose_name_plural = 'evaluations'
        app_label = 'core'