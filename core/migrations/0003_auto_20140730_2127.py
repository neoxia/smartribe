# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140730_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='private',
            field=models.BooleanField(default=True),
        ),
    ]
