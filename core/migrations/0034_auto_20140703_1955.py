# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.profile


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20140703_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to=core.models.profile.get_photo, null=True),
        ),
    ]
