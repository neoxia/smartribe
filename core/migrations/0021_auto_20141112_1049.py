# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20141008_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='inappropriate',
            name='content_identifier',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='inappropriate',
            name='content_url',
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(2, 'Neutral'), (0, 'Dangerous'), (4, 'Excellent'), (5, 'Perfect'), (3, 'Good'), (1, 'Bad')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('R', 'Refused'), ('P', 'Pending'), ('A', 'Accepted')], default='P', max_length=1),
        ),
    ]
