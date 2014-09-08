# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20140902_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(1, 'Bad'), (0, 'Dangerous'), (4, 'Excellent'), (5, 'Perfect'), (3, 'Good'), (2, 'Neutral')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(max_length=1, choices=[('A', 'Accepted'), ('P', 'Pending'), ('R', 'Refused')], default='P'),
        ),
    ]
