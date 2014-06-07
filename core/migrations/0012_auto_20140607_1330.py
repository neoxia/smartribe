# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_request_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='pseudo',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
