# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='community',
            options={'verbose_name_plural': 'communities', 'verbose_name': 'community'},
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name_plural': 'members', 'verbose_name': 'member'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'profiles', 'verbose_name': 'profile'},
        ),
        migrations.AlterModelOptions(
            name='tos',
            options={'verbose_name_plural': 'tos', 'verbose_name': 'tos'},
        ),
    ]
