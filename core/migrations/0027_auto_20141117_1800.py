# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20141117_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='creation_date',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='creation_date',
            new_name='created_on',
        ),
        migrations.AddField(
            model_name='request',
            name='last_update',
            field=models.DateTimeField(auto_now=True, default='1900-01-01T00:00:00+00:00'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(5, 'Perfect'), (3, 'Good'), (1, 'Bad'), (4, 'Excellent'), (0, 'Dangerous'), (2, 'Neutral')]),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('R', 'Refused'), ('A', 'Accepted'), ('P', 'Pending')], default='P', max_length=1),
        ),
    ]
