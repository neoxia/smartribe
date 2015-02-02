# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150202_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(1, 'Bad'), (4, 'Excellent'), (5, 'Perfect'), (2, 'Neutral'), (0, 'Dangerous'), (3, 'Good')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(max_length=1, default='P', choices=[('P', 'Pending'), ('R', 'Refused'), ('A', 'Accepted')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
