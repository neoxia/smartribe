# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20141203_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('offer', models.ForeignKey(to='core.Offer')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'messages',
                'verbose_name': 'message',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='meetingmessage',
            name='offer',
        ),
        migrations.RemoveField(
            model_name='meetingmessage',
            name='user',
        ),
        migrations.DeleteModel(
            name='MeetingMessage',
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(1, 'Bad'), (0, 'Dangerous'), (5, 'Perfect'), (4, 'Excellent'), (2, 'Neutral'), (3, 'Good')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', choices=[('A', 'Accepted'), ('R', 'Refused'), ('P', 'Pending')], max_length=1),
            preserve_default=True,
        ),
    ]
