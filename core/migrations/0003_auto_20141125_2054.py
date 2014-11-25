# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141117_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetingmessage',
            name='meeting',
        ),
        migrations.AddField(
            model_name='meetingmessage',
            name='offer',
            field=models.ForeignKey(default=1, to='core.Offer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(3, 'Good'), (5, 'Perfect'), (0, 'Dangerous'), (1, 'Bad'), (4, 'Excellent'), (2, 'Neutral')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Refused')], default='P', max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile'),
            preserve_default=True,
        ),
    ]
