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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'activation token',
                'verbose_name_plural': 'activation tokens',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, null=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(blank=True, validators=[core.models.validator.ZipCodeValidatorFR()], null=True, max_length=10)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField(max_length=180)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update', models.DateField(auto_now=True)),
                ('auto_accept_member', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'community',
                'verbose_name_plural': 'communities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('private', models.BooleanField(default=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
        migrations.CreateModel(
            name='Inappropriate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('content_url', models.URLField()),
                ('detail', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'inappropriate content',
                'verbose_name_plural': 'inappropriate contents',
            },
            bases=(models.Model,),
        ),
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
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('index', models.IntegerField(blank=True, null=True)),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('community', models.ForeignKey(to='core.Community')),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'meeting',
                'verbose_name_plural': 'meetings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingMessage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('content', models.TextField()),
                ('meeting', models.ForeignKey(to='core.Meeting')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'meeting message',
                'verbose_name_plural': 'meeting messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingPoint',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'meeting point',
                'verbose_name_plural': 'meeting points',
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('role', models.CharField(choices=[('0', 'Owner'), ('1', 'Moderator'), ('2', 'Member')], max_length=10, default='2')),
                ('status', models.CharField(choices=[('0', 'Pending'), ('1', 'Accepted'), ('2', 'Banned')], max_length=10, default='0')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('last_modification_date', models.DateField(auto_now=True)),
                ('community', models.ForeignKey(to='core.Community')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'member',
                'verbose_name_plural': 'members',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('detail', models.TextField()),
                ('creation_date', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'offer',
                'verbose_name_plural': 'offers',
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('ip_address', models.IPAddressField()),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'password recovery',
                'verbose_name_plural': 'password recoveries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=2, default='O')),
                ('phone', models.CharField(blank=True, validators=[core.models.validator.PhoneValidatorFR()], null=True, max_length=15)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=core.models.profile.get_photo_path)),
                ('favorite_contact', models.CharField(choices=[('E', 'Email'), ('P', 'Phone'), ('N', 'None')], max_length=2, default='N')),
                ('address', models.OneToOneField(blank=True, to='core.Address', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                'verbose_name': 'request',
                'verbose_name_plural': 'requests',
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'skill',
                'verbose_name_plural': 'skills',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField()),
            ],
            options={
                'verbose_name': 'skill category',
                'verbose_name_plural': 'skill categories',
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('category', models.CharField(choices=[('B', 'Bug report'), ('U', 'Upgrade'), ('O', 'Others')], max_length=1, default='O')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'suggestion',
                'verbose_name_plural': 'suggestions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('version', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('terms', models.TextField()),
            ],
            options={
                'verbose_name': 'tos',
                'verbose_name_plural': 'tos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransportCommunity',
            fields=[
                ('departure', models.CharField(max_length=255)),
                ('via', models.CharField(blank=True, null=True, max_length=255)),
                ('arrival', models.CharField(max_length=255)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField(blank=True, null=True, max_length=180)),
            ],
            options={
                'verbose_name': 'transport stop',
                'verbose_name_plural': 'transport stops',
            },
            bases=(models.Model,),
        ),
    ]
