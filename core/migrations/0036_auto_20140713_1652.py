# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_activationtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorite_contact',
            field=models.CharField(max_length=2, choices=[('E', 'Email'), ('P', 'Phone'), ('N', 'None')], default='N'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.OneToOneField(null=True, blank=True, to_field='id', to='core.Address'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='address',
            name='profile',
        ),
    ]
