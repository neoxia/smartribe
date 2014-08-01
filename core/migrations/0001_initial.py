# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import core.models.validator
import core.models.profile


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationToken',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('token', models.CharField(max_length=64)),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'activation tokens',
                'verbose_name': 'activation token',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, null=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(blank=True, null=True, validators=[core.models.validator.ZipCodeValidatorFR()], max_length=10)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'addresses',
                'verbose_name': 'address',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField(max_length=180)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('auto_accept_member', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'communities',
                'verbose_name': 'community',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('private', models.BooleanField(default=True)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'frequently asked questions',
                'verbose_name': 'frequently asked question',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqSection',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name_plural': 'FAQ sections',
                'verbose_name': 'FAQ section',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='faq',
            name='section',
            field=models.ForeignKey(to='core.FaqSection'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LocalCommunity',
            fields=[
                ('address', models.ForeignKey(to='core.Address')),
                ('community_ptr', models.OneToOneField(serialize=False, to='core.Community', primary_key=True, auto_created=True)),
            ],
            options={
                'verbose_name_plural': 'local communities',
                'verbose_name': 'local community',
            },
            bases=('core.community',),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('communities', models.ManyToManyField(to='core.Community')),
            ],
            options={
                'verbose_name_plural': 'locations',
                'verbose_name': 'location',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date_time', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'meetings',
                'verbose_name': 'meeting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingMessage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date_time', models.DateTimeField()),
                ('content', models.TextField()),
                ('meeting', models.ForeignKey(to='core.Meeting')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'meeting messages',
                'verbose_name': 'meeting message',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingPoint',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name_plural': 'meeting points',
                'verbose_name': 'meeting point',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_point',
            field=models.ForeignKey(to='core.MeetingPoint'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('role', models.CharField(choices=[('0', 'Owner'), ('1', 'Moderator'), ('2', 'Member')], default='2', max_length=10)),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'Accepted'), ('2', 'Banned')], default='0', max_length=10)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('last_modification_date', models.DateField(auto_now=True)),
                ('community', models.ForeignKey(to='core.Community')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'members',
                'verbose_name': 'member',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('detail', models.TextField()),
                ('creation_date', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'offers',
                'verbose_name': 'offer',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meeting',
            name='offer',
            field=models.ForeignKey(to='core.Offer'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='PasswordRecovery',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('token', models.CharField(max_length=64)),
                ('ip_address', models.IPAddressField()),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'password recoveries',
                'verbose_name': 'password recovery',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O', max_length=2)),
                ('phone', models.CharField(blank=True, null=True, validators=[core.models.validator.PhoneValidatorFR()], max_length=15)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=core.models.profile.get_photo)),
                ('favorite_contact', models.CharField(choices=[('E', 'Email'), ('P', 'Phone'), ('N', 'None')], default='N', max_length=2)),
                ('address', models.OneToOneField(blank=True, to='core.Address', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'profiles',
                'verbose_name': 'profile',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('expected_end_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('auto_close', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'requests',
                'verbose_name': 'request',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='offer',
            name='request',
            field=models.ForeignKey(to='core.Request'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'skills',
                'verbose_name': 'skill',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'skill categories',
                'verbose_name': 'skill category',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='skill',
            name='category',
            field=models.ForeignKey(to='core.SkillCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='category',
            field=models.ForeignKey(to='core.SkillCategory'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('category', models.CharField(choices=[('B', 'Bug report'), ('U', 'Upgrade'), ('O', 'Others')], default='O', max_length=1)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'suggestions',
                'verbose_name': 'suggestion',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('version', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('terms', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'tos',
                'verbose_name': 'tos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransportCommunity',
            fields=[
                ('community_ptr', models.OneToOneField(serialize=False, to='core.Community', primary_key=True, auto_created=True)),
            ],
            options={
                'verbose_name_plural': 'transport communities',
                'verbose_name': 'transport community',
            },
            bases=('core.community',),
        ),
        migrations.CreateModel(
            name='TransportStop',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField(blank=True, null=True, max_length=180)),
            ],
            options={
                'verbose_name_plural': 'transport stops',
                'verbose_name': 'transport stop',
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
