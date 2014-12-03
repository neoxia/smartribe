# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='description',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(1, 'Bad'), (4, 'Excellent'), (0, 'Dangerous'), (2, 'Neutral'), (3, 'Good'), (5, 'Perfect')]),
            preserve_default=True,
        ),
    ]
