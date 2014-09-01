# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default='2014-01-01 00:00:00+01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluation',
            name='last_update',
            field=models.DateTimeField(default='2014-01-01 00:00:00+01', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.CharField(choices=[('1', 'Bad'), ('3', 'Good'), ('2', 'Neutral'), ('4', 'Excellent'), ('0', 'Dangerous'), ('5', 'Perfect')], max_length=1),
        ),
    ]
