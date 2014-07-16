# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('category', models.ForeignKey(to='core.SkillCategory', to_field='id')),
                ('title', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('expected_end_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('auto_close', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'request',
                'verbose_name_plural': 'requests',
            },
            bases=(models.Model,),
        ),
    ]
