# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20140616_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='creator',
        ),
        migrations.AlterField(
            model_name='community',
            name='creation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
