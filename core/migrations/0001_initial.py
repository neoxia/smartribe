# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.meeting_point
import core.models.community
import core.models.profile
import django.utils.timezone
from django.conf import settings
import core.models.validator


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(unique=True, verbose_name='email address', max_length=255)),
                ('first_name', models.CharField(verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', related_query_name='user', verbose_name='groups', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', verbose_name='user permissions', to='auth.Permission')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivationToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('token', models.CharField(max_length=64)),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': "tokens d'activation",
                'verbose_name': "token d'activation",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
                ('banner', models.ImageField(blank=True, null=True, upload_to=core.models.community.get_banner_path)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=core.models.community.get_logo_path)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_update', models.DateField(auto_now=True)),
                ('auto_accept_member', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'communautés',
                'verbose_name': 'communauté',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('mark', models.IntegerField(choices=[(0, 'Dangerous'), (1, 'Bad'), (2, 'Neutral'), (3, 'Good'), (4, 'Excellent'), (5, 'Perfect')])),
                ('usefull', models.BooleanField(default=True)),
                ('comment', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'évaluations',
                'verbose_name': 'évaluation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('private', models.BooleanField(default=True)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'questions fréquentes',
                'verbose_name': 'question fréquente',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FaqSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=70)),
            ],
            options={
                'verbose_name_plural': 'sections de la FAQ',
                'verbose_name': 'section de la FAQ',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inappropriate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('content_identifier', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'contenus inappropriés',
                'verbose_name': 'contenu inapproprié',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalCommunity',
            fields=[
                ('community_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='core.Community')),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, null=True, max_length=100)),
                ('zip_code', models.CharField(blank=True, null=True, validators=[core.models.validator.ZipCodeValidatorFR()], max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('index', models.IntegerField(blank=True, null=True)),
                ('gps_x', models.FloatField()),
                ('gps_y', models.FloatField()),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, null=True, max_length=100)),
                ('zip_code', models.CharField(blank=True, null=True, validators=[core.models.validator.ZipCodeValidatorFR()], max_length=10)),
                ('city', models.CharField(blank=True, null=True, max_length=100)),
                ('country', models.CharField(blank=True, null=True, max_length=50)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date_time', models.DateTimeField()),
                ('status', models.CharField(max_length=1, choices=[('P', 'En attente'), ('A', 'Accepté'), ('R', 'Refusé')], default='P')),
                ('is_validated', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'rendez-vous',
                'verbose_name': 'rendez-vous',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeetingPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=core.models.meeting_point.get_photo_path)),
                ('location', models.ForeignKey(to='core.Location')),
            ],
            options={
                'verbose_name_plural': 'points de rencontre',
                'verbose_name': 'point de rencontre',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('role', models.CharField(max_length=10, choices=[('0', 'Propriétaire'), ('1', 'Modérateur'), ('2', 'Membre')], default='2')),
                ('status', models.CharField(max_length=10, choices=[('0', 'En attente'), ('1', 'Accepté'), ('2', 'Banni')], default='0')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('last_modification_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'membres',
                'verbose_name': 'membre',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'messages',
                'verbose_name': 'message',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('title', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('seen', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('seen_on', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'notifications',
                'verbose_name': 'notification',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('detail', models.TextField()),
                ('closed', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'offres',
                'verbose_name': 'offre',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordRecovery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('token', models.CharField(max_length=64)),
                ('ip_address', models.IPAddressField()),
                ('request_datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'réinitialisations de mot de passe',
                'verbose_name': 'réinitialisation de mot de passe',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('gender', models.CharField(max_length=2, choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], default='O')),
                ('street_num', models.IntegerField(blank=True, null=True)),
                ('street', models.CharField(blank=True, null=True, max_length=100)),
                ('zip_code', models.CharField(blank=True, null=True, validators=[core.models.validator.ZipCodeValidatorFR()], max_length=10)),
                ('city', models.CharField(blank=True, null=True, max_length=100)),
                ('country', models.CharField(blank=True, null=True, max_length=50)),
                ('phone', models.CharField(blank=True, null=True, validators=[core.models.validator.PhoneValidatorFR()], max_length=15)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=core.models.profile.get_photo_path)),
                ('mail_notification', models.BooleanField(default=True)),
                ('favorite_contact', models.CharField(max_length=2, choices=[('E', 'Email'), ('P', 'Téléphone'), ('N', 'Aucun')], default='N')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'profils',
                'verbose_name': 'profil',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                'verbose_name_plural': 'demandes',
                'verbose_name': 'demande',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(choices=[(1, 'Moyen'), (2, 'Elevé'), (3, 'Expert')], default=1)),
            ],
            options={
                'verbose_name_plural': 'compétences',
                'verbose_name': 'compétence',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'catégories de compétence',
                'verbose_name': 'catégorie de compétence',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('category', models.CharField(max_length=1, choices=[('B', 'Signalement de bug'), ('U', 'Amélioration'), ('O', 'Autres')], default='O')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('version', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('terms', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'cgu',
                'verbose_name': 'cgu',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransportCommunity',
            fields=[
                ('community_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, parent_link=True, to='core.Community')),
                ('departure', models.CharField(max_length=255)),
                ('via', models.CharField(blank=True, null=True, max_length=255)),
                ('arrival', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'transport communities',
                'verbose_name': 'transport community',
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
            field=models.ForeignKey(blank=True, null=True, to='core.Community'),
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
            field=models.ForeignKey(blank=True, null=True, to='core.Skill'),
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
