# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150220_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(3, 'Good'), (1, 'Bad'), (4, 'Excellent'), (0, 'Dangerous'), (5, 'Perfect'), (2, 'Neutral')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('A', 'Accepté'), ('R', 'Refusé'), ('P', 'En attente')], max_length=1, default='P'),
            preserve_default=True,
        ),
    ]
