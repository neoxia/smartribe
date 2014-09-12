# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20140902_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.CharField(max_length=1, choices=[('4', 'Excellent'), ('0', 'Dangerous'), ('3', 'Good'), ('5', 'Perfect'), ('1', 'Bad'), ('2', 'Neutral')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('R', 'Refused'), ('A', 'Accepted')], max_length=1, default='P'),
        ),
    ]
