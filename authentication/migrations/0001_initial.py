# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyActivationToken',
            fields=[
            ],
            options={
                'verbose_name_plural': "tokens d'activation",
                'verbose_name': "token d'activation",
                'proxy': True,
            },
            bases=('core.activationtoken',),
        ),
        migrations.CreateModel(
            name='ProxyCustomUser',
            fields=[
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'proxy': True,
            },
            bases=('core.customuser',),
        ),
        migrations.CreateModel(
            name='ProxyPasswordRecovery',
            fields=[
            ],
            options={
                'verbose_name_plural': 'réinitialisations de mot de passe',
                'verbose_name': 'réinitialisation de mot de passe',
                'proxy': True,
            },
            bases=('core.passwordrecovery',),
        ),
    ]
