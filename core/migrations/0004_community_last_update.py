# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20140812_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='last_update',
            field=models.DateField(default='2000-01-01', auto_now=True),
            preserve_default=False,
        ),
    ]
