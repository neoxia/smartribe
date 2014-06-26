# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0029_auto_20140624_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordRecovery',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('token', models.CharField(max_length=64)),
                ('ip_address', models.IPAddressField()),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'password recoveries',
                'verbose_name': 'password recovery',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='community',
            options={'verbose_name_plural': 'communities', 'verbose_name': 'community'},
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name_plural': 'members', 'verbose_name': 'member'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'profiles', 'verbose_name': 'profile'},
        ),
        migrations.AlterModelOptions(
            name='tos',
            options={'verbose_name_plural': 'tos', 'verbose_name': 'tos'},
        ),
    ]
