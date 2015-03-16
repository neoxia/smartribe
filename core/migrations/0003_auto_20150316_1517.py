# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150316_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(0, 'Dangerous'), (1, 'Bad'), (2, 'Neutral'), (3, 'Good'), (4, 'Excellent'), (5, 'Perfect')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', choices=[('P', 'En attente'), ('A', 'Accepté'), ('R', 'Refusé')], max_length=1),
            preserve_default=True,
        ),
    ]
