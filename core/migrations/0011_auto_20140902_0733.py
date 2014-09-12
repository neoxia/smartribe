# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20140901_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', choices=[('A', 'Accepted'), ('R', 'Refused'), ('P', 'Pending')], max_length=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.CharField(choices=[('4', 'Excellent'), ('3', 'Good'), ('1', 'Bad'), ('2', 'Neutral'), ('0', 'Dangerous'), ('5', 'Perfect')], max_length=1),
        ),
    ]
