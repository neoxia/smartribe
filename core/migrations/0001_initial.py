# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.profile
import django.utils.timezone
import core.models.validator
import core.models.community
import core.models.meeting_point
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', unique=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', to='auth.Group', verbose_name='groups', related_name='user_set', blank=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', help_text='Specific permissions for this user.', to='auth.Permission', verbose_name='user permissions', related_name='user_set', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('token', models.CharField(max_length=64)),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "token d'activation",
                'verbose_name_plural': "tokens d'activation",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('banner', models.ImageField(blank=True, upload_to=core.models.community.get_banner_path, null=True)),
                ('logo', models.ImageField(blank=True, upload_to=core.models.community.get_logo_path, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update', models.DateField(auto_now=True)),
                ('auto_accept_member', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'communauté',
                'verbose_name_plural': 'communautés',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('mark', models.IntegerField(choices=[(2, 'Neutral'), (0, 'Dangerous'), (4, 'Excellent'), (5, 'Perfect'), (3, 'Good'), (1, 'Bad')])),
                ('usefull', models.BooleanField(default=True)),
                ('comment', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'évaluation',
                'verbose_name_plural': 'évaluations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('private', models.BooleanField(default=True)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'question fréquente',
                'verbose_name_plural': 'questions fréquentes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name': 'section de la FAQ',
                'verbose_name_plural': 'sections de la FAQ',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inappropriate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('content_identifier', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'contenu inapproprié',
                'verbose_name_plural': 'contenus inappropriés',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalCommunity',
            fields=[
                ('community_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='core.Community')),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(max_length=100, blank=True, null=True)),
                ('zip_code', models.CharField(max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], blank=True, null=True)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('index', models.IntegerField(blank=True, null=True)),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(max_length=100, blank=True, null=True)),
                ('zip_code', models.CharField(max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], blank=True, null=True)),
                ('city', models.CharField(max_length=100, blank=True, null=True)),
                ('country', models.CharField(max_length=50, blank=True, null=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_time', models.DateTimeField()),
                ('status', models.CharField(max_length=1, choices=[('P', 'En attente'), ('A', 'Accepté'), ('R', 'Refusé')], default='P')),
                ('is_validated', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'rendez-vous',
                'verbose_name_plural': 'rendez-vous',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to=core.models.meeting_point.get_photo_path, null=True)),
                ('location', models.ForeignKey(to='core.Location')),
            ],
            options={
                'verbose_name': 'point de rencontre',
                'verbose_name_plural': 'points de rencontre',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('role', models.CharField(max_length=10, choices=[('0', 'Propriétaire'), ('1', 'Modérateur'), ('2', 'Membre')], default='2')),
                ('status', models.CharField(max_length=10, choices=[('0', 'En attente'), ('1', 'Accepté'), ('2', 'Banni')], default='0')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('last_modification_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'membre',
                'verbose_name_plural': 'membres',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('photo', models.ImageField(blank=True, upload_to='', null=True)),
                ('title', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('seen', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('seen_on', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('detail', models.TextField()),
                ('closed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'offre',
                'verbose_name_plural': 'offres',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordRecovery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('token', models.CharField(max_length=64)),
                ('ip_address', models.IPAddressField()),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'réinitialisation de mot de passe',
                'verbose_name_plural': 'réinitialisations de mot de passe',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('gender', models.CharField(max_length=2, choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], default='O')),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(max_length=100, blank=True, null=True)),
                ('zip_code', models.CharField(max_length=10, validators=[core.models.validator.ZipCodeValidatorFR()], blank=True, null=True)),
                ('city', models.CharField(max_length=100, blank=True, null=True)),
                ('country', models.CharField(max_length=50, blank=True, null=True)),
                ('phone', models.CharField(max_length=15, validators=[core.models.validator.PhoneValidatorFR()], blank=True, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to=core.models.profile.get_photo_path, null=True)),
                ('mail_notification', models.BooleanField(default=True)),
                ('favorite_contact', models.CharField(max_length=2, choices=[('E', 'Email'), ('P', 'Téléphone'), ('N', 'Aucun')], default='N')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
                'verbose_name': 'profil',
                'verbose_name_plural': 'profils',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('created_on', models.DateField(auto_now_add=True)),
                ('expected_end_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('auto_close', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'demande',
                'verbose_name_plural': 'demandes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(choices=[(1, 'Moyen'), (2, 'Elevé'), (3, 'Expert')], default=1)),
            ],
            options={
                'verbose_name': 'compétence',
                'verbose_name_plural': 'compétences',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField()),
            ],
            options={
                'verbose_name': 'catégorie de compétence',
                'verbose_name_plural': 'catégories de compétence',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('category', models.CharField(max_length=1, choices=[('B', 'Signalement de bug'), ('U', 'Amélioration'), ('O', 'Autres')], default='O')),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('version', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('terms', models.TextField()),
            ],
            options={
                'verbose_name': 'cgu',
                'verbose_name_plural': 'cgu',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransportCommunity',
            fields=[
                ('community_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='core.Community')),
                ('departure', models.CharField(max_length=255)),
                ('via', models.CharField(max_length=255, blank=True, null=True)),
                ('arrival', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'transport community',
                'verbose_name_plural': 'transport communities',
            },
            bases=('core.community',),
        ),
        migrations.AddField(
            model_name='skill',
            name='category',
            field=models.ForeignKey(to='core.SkillCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='category',
            field=models.ForeignKey(to='core.SkillCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='community',
            field=models.ForeignKey(to='core.Community', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='request',
            field=models.ForeignKey(to='core.Request'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='skill',
            field=models.ForeignKey(to='core.Skill', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='offer',
            field=models.ForeignKey(to='core.Offer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='community',
            field=models.ForeignKey(to='core.Community'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_point',
            field=models.ForeignKey(to='core.MeetingPoint'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='offer',
            field=models.ForeignKey(to='core.Offer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meeting',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='community',
            field=models.ForeignKey(to='core.Community'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faq',
            name='section',
            field=models.ForeignKey(to='core.FaqSection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evaluation',
            name='offer',
            field=models.ForeignKey(to='core.Offer'),
            preserve_default=True,
        ),
    ]
