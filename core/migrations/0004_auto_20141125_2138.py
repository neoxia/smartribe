# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141125_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='meeting',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='offer',
            field=models.ForeignKey(default=0, to='core.Offer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(4, 'Excellent'), (1, 'Bad'), (0, 'Dangerous'), (5, 'Perfect'), (2, 'Neutral'), (3, 'Good')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('R', 'Refused'), ('P', 'Pending')], default='P', max_length=1),
            preserve_default=True,
        ),
    ]
