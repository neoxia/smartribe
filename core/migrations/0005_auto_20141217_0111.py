# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20141209_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='usefull',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='usefull',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(2, 'Neutral'), (5, 'Perfect'), (4, 'Excellent'), (3, 'Good'), (0, 'Dangerous'), (1, 'Bad')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', max_length=1, choices=[('R', 'Refused'), ('A', 'Accepted'), ('P', 'Pending')]),
            preserve_default=True,
        ),
    ]
