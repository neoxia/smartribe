# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20140607_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id', null=True),
        ),
    ]
