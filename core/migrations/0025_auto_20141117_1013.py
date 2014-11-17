# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.validator


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20141117_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='street_num',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='street_num',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(3, 'Good'), (4, 'Excellent'), (2, 'Neutral'), (1, 'Bad'), (0, 'Dangerous'), (5, 'Perfect')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(max_length=1, choices=[('R', 'Refused'), ('A', 'Accepted'), ('P', 'Pending')], default='P'),
        ),
    ]
