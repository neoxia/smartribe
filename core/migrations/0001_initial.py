# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.community
import core.models.profile
import core.models.meeting_point
import core.models.validator
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationToken',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(blank=True, max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], null=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(max_length=180)),
                ('banner', models.ImageField(blank=True, upload_to=core.models.community.get_banner_path, null=True)),
                ('logo', models.ImageField(blank=True, upload_to=core.models.community.get_logo_path, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update', models.DateField(auto_now=True)),
                ('auto_accept_member', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'communities',
                'verbose_name': 'community',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('mark', models.IntegerField(choices=[(0, 'Dangerous'), (3, 'Good'), (4, 'Excellent'), (2, 'Neutral'), (1, 'Bad'), (5, 'Perfect')])),
                ('comment', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'evaluations',
                'verbose_name': 'evaluation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
            name='Inappropriate',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('content_identifier', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'inappropriate contents',
                'verbose_name': 'inappropriate content',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalCommunity',
            fields=[
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], null=True)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
                ('community_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, to='core.Community')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('index', models.IntegerField(blank=True, null=True)),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('community', models.ForeignKey(to='core.Community')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('status', models.CharField(max_length=1, default='P', choices=[('R', 'Refused'), ('P', 'Pending'), ('A', 'Accepted')])),
                ('is_validated', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'meetings',
                'verbose_name': 'meeting',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='meeting',
            field=models.ForeignKey(to='core.Meeting'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='MeetingMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, upload_to=core.models.meeting_point.get_photo_path, null=True)),
                ('location', models.ForeignKey(to='core.Location')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('role', models.CharField(max_length=10, default='2', choices=[('0', 'Owner'), ('1', 'Moderator'), ('2', 'Member')])),
                ('status', models.CharField(max_length=10, default='0', choices=[('0', 'Pending'), ('1', 'Accepted'), ('2', 'Banned')])),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('detail', models.TextField()),
                ('closed', models.BooleanField(default=False)),
                ('usefull', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('gender', models.CharField(max_length=2, default='O', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, validators=[core.models.validator.PhoneValidatorFR()], null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to=core.models.profile.get_photo_path, null=True)),
                ('favorite_contact', models.CharField(max_length=2, default='N', choices=[('E', 'Email'), ('P', 'Phone'), ('N', 'None')])),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('created_on', models.DateField(auto_now_add=True)),
                ('expected_end_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('auto_close', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(blank=True, null=True, to='core.Community')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.TextField()),
                ('level', models.IntegerField(default=1, choices=[(1, 'Medium'), (2, 'High'), (3, 'Expert')])),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('category', models.CharField(max_length=1, default='O', choices=[('B', 'Bug report'), ('U', 'Upgrade'), ('O', 'Others')])),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('departure', models.CharField(max_length=255)),
                ('via', models.CharField(blank=True, max_length=255, null=True)),
                ('arrival', models.CharField(max_length=255)),
                ('community_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, to='core.Community')),
            ],
            options={
                'verbose_name_plural': 'transport communities',
                'verbose_name': 'transport community',
            },
            bases=('core.community',),
        ),
    ]
