# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20140826_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingmessage',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
