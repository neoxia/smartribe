# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20140616_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField()),
            ],
            options={
                'verbose_name': 'skill category',
                'verbose_name_plural': 'skill categories',
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='offer',
            old_name='description',
            new_name='detail',
        ),
        migrations.AddField(
            model_name='request',
            name='expected_end_date',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='end_date',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='auto_close',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='request',
            old_name='description',
            new_name='detail',
        ),
        migrations.AddField(
            model_name='offer',
            name='creation_date',
            field=models.TextField(default='1900-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='creation_date',
            field=models.DateField(auto_now_add=True, default='1900-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skill',
            name='category',
            field=models.ForeignKey(to_field='id', default=1, to='core.SkillCategory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='category',
            field=models.ForeignKey(to_field='id', default=1, to='core.SkillCategory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(to_field='id', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='closed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='description',
            field=models.TextField(max_length=180),
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='request',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
