# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_community_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='banner',
            field=models.ImageField(blank=True, upload_to='', null=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='logo',
            field=models.ImageField(blank=True, upload_to='', null=True),
        ),
    ]
