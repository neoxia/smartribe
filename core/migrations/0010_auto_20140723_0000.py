# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20140722_2026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('communities', models.ManyToManyField(to='core.Community')),
            ],
            options={
                'verbose_name_plural': 'locations',
                'verbose_name': 'location',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date_time', models.DateTimeField()),
                ('offer', models.ForeignKey(to='core.Offer')),
            ],
            options={
                'verbose_name_plural': 'meetings',
                'verbose_name': 'meeting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date_time', models.DateTimeField()),
                ('content', models.TextField()),
                ('meeting', models.ForeignKey(to='core.Meeting')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'meeting messages',
                'verbose_name': 'meeting message',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name_plural': 'meeting points',
                'verbose_name': 'meeting point',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_point',
            field=models.ForeignKey(to='core.MeetingPoint'),
            preserve_default=True,
        ),
    ]
