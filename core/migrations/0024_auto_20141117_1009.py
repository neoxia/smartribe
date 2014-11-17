# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.validator


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20141114_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='localcommunity',
            name='city',
            field=models.CharField(max_length=100, default='Paris'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localcommunity',
            name='country',
            field=models.CharField(max_length=50, default='France'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localcommunity',
            name='gps_x',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localcommunity',
            name='gps_y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localcommunity',
            name='street',
            field=models.CharField(null=True, blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='localcommunity',
            name='street_num',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='localcommunity',
            name='zip_code',
            field=models.CharField(null=True, validators=[core.models.validator.ZipCodeValidatorFR()], blank=True, max_length=10),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='localcommunity',
            name='address',
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(4, 'Excellent'), (5, 'Perfect'), (0, 'Dangerous'), (1, 'Bad'), (3, 'Good'), (2, 'Neutral')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(max_length=1, choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Refused')], default='P'),
        ),
    ]
