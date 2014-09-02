# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20140902_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.CharField(max_length=1, choices=[('0', 'Dangerous'), ('2', 'Neutral'), ('1', 'Bad'), ('3', 'Good'), ('4', 'Excellent'), ('5', 'Perfect')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(max_length=1, choices=[('R', 'Refused'), ('P', 'Pending'), ('A', 'Accepted')], default='P'),
        ),
    ]
