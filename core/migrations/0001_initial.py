# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings
import django.utils.timezone
import core.models.validator
import core.models.profile


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(verbose_name='email address', max_length=255, unique=True)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], max_length=32, unique=True, help_text='Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'})),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', blank=True, to='auth.Permission')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('num', models.IntegerField(null=True, blank=True)),
                ('street', models.CharField(null=True, blank=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(null=True, blank=True, max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()])),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(max_length=180)),
                ('banner', models.ImageField(null=True, upload_to='', blank=True)),
                ('logo', models.ImageField(null=True, upload_to='', blank=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('auto_accept_member', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'community',
                'verbose_name_plural': 'communities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalCommunity',
            fields=[
                ('address', models.ForeignKey(to='core.Address')),
                ('community_ptr', models.OneToOneField(to='core.Community', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('communities', models.ManyToManyField(to='core.Community')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=2, default='O')),
                ('phone', models.CharField(null=True, blank=True, max_length=15, validators=[core.models.validator.PhoneValidatorFR()])),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('bio', models.TextField(null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=core.models.profile.get_photo, blank=True)),
                ('favorite_contact', models.CharField(choices=[('E', 'Email'), ('P', 'Phone'), ('N', 'None')], max_length=2, default='N')),
                ('address', models.OneToOneField(null=True, to='core.Address', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('expected_end_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
            name='Tos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
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
                ('community_ptr', models.OneToOneField(to='core.Community', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField(null=True, blank=True, max_length=180)),
            ],
            options={
                'verbose_name': 'transport stop',
                'verbose_name_plural': 'transport stops',
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
