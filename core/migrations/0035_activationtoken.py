# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0034_auto_20140703_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationToken',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('token', models.CharField(max_length=64)),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'activation token',
                'verbose_name_plural': 'activation tokens',
            },
            bases=(models.Model,),
        ),
    ]
