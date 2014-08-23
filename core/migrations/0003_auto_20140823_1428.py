# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140822_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingpoint',
            name='photo',
            field=models.ImageField(upload_to='', blank=True, null=True),
        ),
    ]
