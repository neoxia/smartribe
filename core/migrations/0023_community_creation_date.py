# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20140616_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='creation_date',
            field=models.DateField(blank=True, auto_created=True, null=True),
            preserve_default=True,
        ),
    ]
