from django.db import models


class FaqSection(models.Model):

    title = models.CharField(max_length=70)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ section'
        verbose_name_plural = 'FAQ sections'
        app_label = 'core'


class Faq(models.Model):

    section = models.ForeignKey(FaqSection)

    private = models.BooleanField(default=True)

    question = models.CharField(max_length=255)

    answer = models.TextField()

    creation_date = models.DateTimeField(auto_now_add=True)

    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'frequently asked question'
        verbose_name_plural = 'frequently asked questions'
        app_label = 'core'
