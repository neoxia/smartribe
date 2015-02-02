# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150202_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(4, 'Excellent'), (5, 'Perfect'), (2, 'Neutral'), (0, 'Dangerous'), (1, 'Bad'), (3, 'Good')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(max_length=1, choices=[('A', 'Accepted'), ('R', 'Refused'), ('P', 'Pending')], default='P'),
            preserve_default=True,
        ),
    ]
