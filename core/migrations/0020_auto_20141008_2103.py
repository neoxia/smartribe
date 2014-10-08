# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20140923_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(5, 'Perfect'), (2, 'Neutral'), (1, 'Bad'), (4, 'Excellent'), (0, 'Dangerous'), (3, 'Good')]),
        ),
    ]
