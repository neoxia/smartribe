# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20140514_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(default='1900-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='no text'),
            preserve_default=False,
        ),
    ]
