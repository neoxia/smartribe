# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20140917_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(1, 'Bad'), (0, 'Dangerous'), (5, 'Perfect'), (3, 'Good'), (4, 'Excellent'), (2, 'Neutral')]),
        ),
    ]
