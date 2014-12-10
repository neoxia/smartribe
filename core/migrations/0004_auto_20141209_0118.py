# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141205_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='skill',
            field=models.ForeignKey(blank=True, to='core.Skill', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(5, 'Perfect'), (3, 'Good'), (0, 'Dangerous'), (2, 'Neutral'), (4, 'Excellent'), (1, 'Bad')]),
            preserve_default=True,
        ),
    ]
