# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_auto_20140607_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='creator',
            field=models.OneToOneField(to_field='id', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
