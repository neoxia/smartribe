# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_meeting_is_validated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('mark', models.CharField(choices=[('5', 'Perfect'), ('4', 'Excellent'), ('1', 'Bad'), ('2', 'Neutral'), ('3', 'Good'), ('0', 'Dangerous')], max_length=1)),
                ('comment', models.TextField()),
                ('meeting', models.ForeignKey(to='core.Meeting')),
            ],
            options={
                'verbose_name_plural': 'evaluations',
                'verbose_name': 'evaluation',
            },
            bases=(models.Model,),
        ),
    ]
