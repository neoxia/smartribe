# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20140616_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='auto_accept_member',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
