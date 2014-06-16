# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0020_remove_profile_pseudo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('registration_date', models.DateField(auto_created=True)),
                ('user', models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('community', models.ForeignKey(to_field='id', to='core.Community')),
                ('status', models.CharField(max_length=10, default=2, choices=[(0, 'Owner'), (1, 'Moderator'), (2, 'Member')])),
                ('last_modification_date', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
