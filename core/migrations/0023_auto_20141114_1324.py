# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20141112_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='closed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='usefull',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(2, 'Neutral'), (4, 'Excellent'), (0, 'Dangerous'), (5, 'Perfect'), (3, 'Good'), (1, 'Bad')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(max_length=1, default='P', choices=[('P', 'Pending'), ('R', 'Refused'), ('A', 'Accepted')]),
        ),
    ]
