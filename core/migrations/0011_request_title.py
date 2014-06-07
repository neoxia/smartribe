# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='title',
            field=models.CharField(max_length=50, default='Contenu'),
            preserve_default=False,
        ),
    ]
