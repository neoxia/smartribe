# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.validator


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20140713_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(blank=True, null=True, validators=[core.models.validator.ZipCodeValidatorFR()], max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='num',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
