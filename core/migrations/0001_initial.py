# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.validator


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tos',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('terms', models.TextField()),
            ],
            options={
                'verbose_name': 'tos',
                'verbose_name_plural': 'tos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, null=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(validators=[core.models.validator.ZipCodeValidatorFR()], null=True, max_length=10, blank=True)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField(max_length=180)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('auto_accept_member', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'community',
                'verbose_name_plural': 'communities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField()),
            ],
            options={
                'verbose_name': 'skill category',
                'verbose_name_plural': 'skill categories',
            },
            bases=(models.Model,),
        ),
    ]
