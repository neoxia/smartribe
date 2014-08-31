# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20140831_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meetingmessage',
            old_name='date_time',
            new_name='creation_date',
        ),
    ]
