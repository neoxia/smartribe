# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150316_1517'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyActivationToken',
            fields=[
            ],
            options={
                'verbose_name': "token d'activation",
                'verbose_name_plural': "tokens d'activation",
                'proxy': True,
            },
            bases=('core.activationtoken',),
        ),
        migrations.CreateModel(
            name='ProxyPasswordRecovery',
            fields=[
            ],
            options={
                'verbose_name': 'réinitialisation de mot de passe',
                'verbose_name_plural': 'réinitialisations de mot de passe',
                'proxy': True,
            },
            bases=('core.passwordrecovery',),
        ),
    ]
