# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150220_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(0, 'Dangerous'), (1, 'Bad'), (4, 'Excellent'), (5, 'Perfect'), (2, 'Neutral'), (3, 'Good')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', choices=[('P', 'En attente'), ('R', 'Refusé'), ('A', 'Accepté')], max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meetingpoint',
            name='description',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
