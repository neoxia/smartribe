# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20140917_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, 'Medium'), (2, 'High'), (3, 'Expert')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(3, 'Good'), (0, 'Dangerous'), (4, 'Excellent'), (5, 'Perfect'), (2, 'Neutral'), (1, 'Bad')]),
        ),
    ]
