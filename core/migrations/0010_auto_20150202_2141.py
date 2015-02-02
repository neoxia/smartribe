# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150202_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(2, 'Neutral'), (3, 'Good'), (0, 'Dangerous'), (4, 'Excellent'), (5, 'Perfect'), (1, 'Bad')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('P', 'Pending'), ('R', 'Refused')], default='P', max_length=1),
            preserve_default=True,
        ),
    ]
