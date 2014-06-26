# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.validator


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_passwordrecovery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('profile', models.OneToOneField(to_field='id', to='core.Profile')),
                ('num', models.IntegerField()),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(validators=[core.models.validator.ZipCodeValidatorFR()], max_length=10)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(validators=[core.models.validator.PhoneValidatorFR()], null=True, max_length=15, blank=True),
            preserve_default=True,
        ),
    ]
