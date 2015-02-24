# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150223_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='photo',
            field=models.ImageField(null=True, blank=True, upload_to=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(default='Titre', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(4, 'Excellent'), (3, 'Good'), (0, 'Dangerous'), (5, 'Perfect'), (2, 'Neutral'), (1, 'Bad')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', max_length=1, choices=[('R', 'Refusé'), ('P', 'En attente'), ('A', 'Accepté')]),
            preserve_default=True,
        ),
    ]
