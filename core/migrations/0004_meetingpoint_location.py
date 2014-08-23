# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20140823_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingpoint',
            name='location',
            field=models.ForeignKey(default=1, to='core.Location'),
            preserve_default=False,
        ),
    ]
