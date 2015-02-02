# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150202_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='seen',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(0, 'Dangerous'), (5, 'Perfect'), (2, 'Neutral'), (3, 'Good'), (4, 'Excellent'), (1, 'Bad')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', choices=[('A', 'Accepted'), ('R', 'Refused'), ('P', 'Pending')], max_length=1),
            preserve_default=True,
        ),
    ]
