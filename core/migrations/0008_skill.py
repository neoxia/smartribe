# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_offer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('category', models.ForeignKey(to='core.SkillCategory', to_field='id')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'skill',
                'verbose_name_plural': 'skills',
            },
            bases=(models.Model,),
        ),
    ]
