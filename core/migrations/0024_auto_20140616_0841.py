# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_community_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='creation_date',
            field=models.DateField(auto_created=True),
        ),
    ]
