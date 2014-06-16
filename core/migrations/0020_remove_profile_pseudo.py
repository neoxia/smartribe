# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20140607_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='pseudo',
        ),
    ]
