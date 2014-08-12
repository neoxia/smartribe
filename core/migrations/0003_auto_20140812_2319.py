# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_inappropriate'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportcommunity',
            name='arrival',
            field=models.CharField(max_length=255, default='end'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transportcommunity',
            name='departure',
            field=models.CharField(max_length=255, default='start'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transportcommunity',
            name='via',
            field=models.CharField(max_length=255, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='transportcommunity',
            name='transport_stop_arrival',
        ),
        migrations.RemoveField(
            model_name='transportcommunity',
            name='transport_stop_departure',
        ),
        migrations.RemoveField(
            model_name='transportcommunity',
            name='transport_stop_via',
        ),
    ]
