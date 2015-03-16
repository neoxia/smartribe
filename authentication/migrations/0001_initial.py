# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150316_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyCustomUser',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=('core.customuser',),
        ),
    ]
