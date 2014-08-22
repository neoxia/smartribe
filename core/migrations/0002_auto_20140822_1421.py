# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='last_update',
            field=models.DateTimeField(default='2014-01-01 00:00:00+01', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='offer',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
