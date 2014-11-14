# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20141112_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(0, 'Dangerous'), (5, 'Perfect'), (1, 'Bad'), (4, 'Excellent'), (3, 'Good'), (2, 'Neutral')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('R', 'Refused'), ('A', 'Accepted'), ('P', 'Pending')], max_length=1, default='P'),
        ),
    ]
