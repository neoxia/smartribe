# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(3, 'Good'), (5, 'Perfect'), (1, 'Bad'), (0, 'Dangerous'), (4, 'Excellent'), (2, 'Neutral')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(max_length=1, default='P', choices=[('P', 'Pending'), ('R', 'Refused'), ('A', 'Accepted')]),
        ),
    ]
