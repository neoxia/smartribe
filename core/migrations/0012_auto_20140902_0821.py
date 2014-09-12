# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.community


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20140902_0733'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TransportStop',
        ),
        migrations.AlterField(
            model_name='community',
            name='banner',
            field=models.ImageField(null=True, blank=True, upload_to=core.models.community.get_banner_path),
        ),
        migrations.AlterField(
            model_name='community',
            name='logo',
            field=models.ImageField(null=True, blank=True, upload_to=core.models.community.get_logo_path),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.CharField(choices=[('3', 'Good'), ('2', 'Neutral'), ('1', 'Bad'), ('0', 'Dangerous'), ('4', 'Excellent'), ('5', 'Perfect')], max_length=1),
        ),
    ]
