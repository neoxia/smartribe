# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150220_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(5, 'Perfect'), (0, 'Dangerous'), (3, 'Good'), (1, 'Bad'), (2, 'Neutral'), (4, 'Excellent')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('P', 'En attente'), ('A', 'Accepté'), ('R', 'Refusé')], default='P', max_length=1),
            preserve_default=True,
        ),
    ]
