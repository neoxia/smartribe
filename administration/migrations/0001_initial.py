# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyFaq',
            fields=[
            ],
            options={
                'verbose_name_plural': 'questions fréquentes',
                'verbose_name': 'question fréquente',
                'proxy': True,
            },
            bases=('core.faq',),
        ),
        migrations.CreateModel(
            name='ProxyFaqSection',
            fields=[
            ],
            options={
                'verbose_name_plural': 'sections de la FAQ',
                'verbose_name': 'section de la FAQ',
                'proxy': True,
            },
            bases=('core.faqsection',),
        ),
        migrations.CreateModel(
            name='ProxyInappropriate',
            fields=[
            ],
            options={
                'verbose_name_plural': 'contenus inappropriés',
                'verbose_name': 'contenu inapproprié',
                'proxy': True,
            },
            bases=('core.inappropriate',),
        ),
        migrations.CreateModel(
            name='ProxySuggestion',
            fields=[
            ],
            options={
                'verbose_name_plural': 'suggestions',
                'verbose_name': 'suggestion',
                'proxy': True,
            },
            bases=('core.suggestion',),
        ),
        migrations.CreateModel(
            name='ProxyTos',
            fields=[
            ],
            options={
                'verbose_name_plural': 'cgu',
                'verbose_name': 'cgu',
                'proxy': True,
            },
            bases=('core.tos',),
        ),
    ]
