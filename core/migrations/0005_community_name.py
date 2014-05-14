# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='name',
            field=models.CharField(default='noname', max_length=50),
            preserve_default=False,
        ),
    ]
