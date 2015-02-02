# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20141217_0111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('message', models.CharField(max_length=255)),
                ('link', models.TextField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'notifications',
                'verbose_name': 'notification',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(1, 'Bad'), (3, 'Good'), (5, 'Perfect'), (4, 'Excellent'), (2, 'Neutral'), (0, 'Dangerous')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', max_length=1, choices=[('A', 'Accepted'), ('P', 'Pending'), ('R', 'Refused')]),
            preserve_default=True,
        ),
    ]
