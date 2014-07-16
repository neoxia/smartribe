# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import core.models.profile
from django.conf import settings
import core.models.validator


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_passwordrecovery'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=2, default='O')),
                ('address', models.OneToOneField(blank=True, null=True, to='core.Address', to_field='id')),
                ('phone', models.CharField(validators=[core.models.validator.PhoneValidatorFR()], null=True, max_length=15, blank=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=core.models.profile.get_photo)),
                ('favorite_contact', models.CharField(choices=[('E', 'Email'), ('P', 'Phone'), ('N', 'None')], max_length=2, default='N')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
            bases=(models.Model,),
        ),
    ]
