# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20141117_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='community',
            field=models.ForeignKey(to='core.Community', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(2, 'Neutral'), (5, 'Perfect'), (0, 'Dangerous'), (1, 'Bad'), (3, 'Good'), (4, 'Excellent')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Refused')], max_length=1),
        ),
    ]
