# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('request', models.ForeignKey(to='core.Request', to_field='id')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'offers',
                'verbose_name': 'offer',
            },
            bases=(models.Model,),
        ),
    ]
