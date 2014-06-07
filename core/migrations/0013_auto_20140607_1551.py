# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20140607_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='logo',
            field=models.ImageField(null=True, upload_to=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='banner',
            field=models.ImageField(null=True, upload_to=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='description',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]
