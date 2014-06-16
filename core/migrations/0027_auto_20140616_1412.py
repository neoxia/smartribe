# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20140616_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='registration_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.CharField(default='0', max_length=10, choices=[('0', 'Pending'), ('1', 'Accepted'), ('2', 'Banned')]),
        ),
    ]
