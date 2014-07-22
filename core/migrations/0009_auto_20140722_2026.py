# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_skill'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalCommunity',
            fields=[
                ('address', models.ForeignKey(to='core.Address')),
                ('community_ptr', models.OneToOneField(serialize=False, to='core.Community', auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'local community',
                'verbose_name_plural': 'local communities',
            },
            bases=('core.community',),
        ),
        migrations.CreateModel(
            name='TransportCommunity',
            fields=[
                ('community_ptr', models.OneToOneField(serialize=False, to='core.Community', auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'transport community',
                'verbose_name_plural': 'transport communities',
            },
            bases=('core.community',),
        ),
        migrations.CreateModel(
            name='TransportStop',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField(blank=True, null=True, max_length=180)),
            ],
            options={
                'verbose_name': 'transport stop',
                'verbose_name_plural': 'transport stops',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transportcommunity',
            name='transport_stop_via',
            field=models.ForeignKey(to='core.TransportStop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transportcommunity',
            name='transport_stop_departure',
            field=models.ForeignKey(to='core.TransportStop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transportcommunity',
            name='transport_stop_arrival',
            field=models.ForeignKey(to='core.TransportStop'),
            preserve_default=True,
        ),
    ]
