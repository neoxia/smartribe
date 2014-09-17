# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20140908_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(4, 'Excellent'), (0, 'Dangerous'), (2, 'Neutral'), (3, 'Good'), (1, 'Bad'), (5, 'Perfect')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('R', 'Refused'), ('P', 'Pending'), ('A', 'Accepted')], default='P', max_length=1),
        ),
    ]
