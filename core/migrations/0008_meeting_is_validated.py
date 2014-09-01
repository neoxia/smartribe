# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20140831_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='is_validated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
