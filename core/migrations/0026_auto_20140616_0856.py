# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_community_auto_accept_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('0', 'Owner'), ('1', 'Moderator'), ('2', 'Member')], default='2', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.CharField(choices=[('0', 'Pending'), ('1', 'Accepted'), ('2', 'Banned')], default='2', max_length=10),
        ),
    ]
