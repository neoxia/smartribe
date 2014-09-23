# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.location


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20140923_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(1, 'Bad'), (4, 'Excellent'), (2, 'Neutral'), (5, 'Perfect'), (3, 'Good'), (0, 'Dangerous')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('R', 'Refused'), ('A', 'Accepted'), ('P', 'Pending')], default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='meetingpoint',
            name='photo',
            field=models.ImageField(null=True, upload_to=core.models.location.get_photo_path, blank=True),
        ),
    ]
