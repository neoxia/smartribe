# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.CharField(default='2', choices=[('0', 'Owner'), ('1', 'Moderator'), ('2', 'Member')], max_length=10),
        ),
    ]
