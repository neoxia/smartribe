# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('private', models.BooleanField(default=False)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'frequently asked question',
                'verbose_name_plural': 'frequently asked questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqSection',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name': 'FAQ section',
                'verbose_name_plural': 'FAQ sections',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='faq',
            name='section',
            field=models.ForeignKey(to='core.FaqSection'),
            preserve_default=True,
        ),
    ]
