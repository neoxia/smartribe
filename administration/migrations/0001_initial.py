# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150316_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyFaq',
            fields=[
            ],
            options={
                'verbose_name_plural': 'questions fréquentes',
                'proxy': True,
                'verbose_name': 'question fréquente',
            },
            bases=('core.faq',),
        ),
        migrations.CreateModel(
            name='ProxyFaqSection',
            fields=[
            ],
            options={
                'verbose_name_plural': 'sections de la FAQ',
                'proxy': True,
                'verbose_name': 'section de la FAQ',
            },
            bases=('core.faqsection',),
        ),
        migrations.CreateModel(
            name='ProxyInappropriate',
            fields=[
            ],
            options={
                'verbose_name_plural': 'contenus inappropriés',
                'proxy': True,
                'verbose_name': 'contenu inapproprié',
            },
            bases=('core.inappropriate',),
        ),
        migrations.CreateModel(
            name='ProxySuggestion',
            fields=[
            ],
            options={
                'verbose_name_plural': 'suggestions',
                'proxy': True,
                'verbose_name': 'suggestion',
            },
            bases=('core.suggestion',),
        ),
        migrations.CreateModel(
            name='ProxyTos',
            fields=[
            ],
            options={
                'verbose_name_plural': 'cgu',
                'proxy': True,
                'verbose_name': 'cgu',
            },
            bases=('core.tos',),
        ),
    ]
