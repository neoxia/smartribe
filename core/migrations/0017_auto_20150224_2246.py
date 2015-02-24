# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20150224_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='seen_on',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(2, 'Neutral'), (3, 'Good'), (5, 'Perfect'), (1, 'Bad'), (4, 'Excellent'), (0, 'Dangerous')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', choices=[('A', 'Accepté'), ('R', 'Refusé'), ('P', 'En attente')], max_length=1),
            preserve_default=True,
        ),
    ]
