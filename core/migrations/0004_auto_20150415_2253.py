# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_donation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='text',
            options={'verbose_name_plural': 'textes', 'verbose_name': 'texte'},
        ),
    ]
