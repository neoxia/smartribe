# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='email address', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(1, 'Bad'), (5, 'Perfect'), (4, 'Excellent'), (2, 'Neutral'), (3, 'Good'), (0, 'Dangerous')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(choices=[('R', 'Refusé'), ('A', 'Accepté'), ('P', 'En attente')], max_length=1, default='P'),
            preserve_default=True,
        ),
    ]
