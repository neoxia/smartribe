# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150202_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mail_notification',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(3, 'Good'), (0, 'Dangerous'), (2, 'Neutral'), (1, 'Bad'), (5, 'Perfect'), (4, 'Excellent')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Refused')], default='P', max_length=1),
            preserve_default=True,
        ),
    ]
