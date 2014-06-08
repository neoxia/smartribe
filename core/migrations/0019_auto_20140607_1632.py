# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20140607_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pseudo',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(null=True, blank=True),
        ),
    ]
