# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150202_2221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activationtoken',
            options={'verbose_name_plural': "tokens d'activation", 'verbose_name': "token d'activation"},
        ),
        migrations.AlterModelOptions(
            name='community',
            options={'verbose_name_plural': 'communautés', 'verbose_name': 'communauté'},
        ),
        migrations.AlterModelOptions(
            name='evaluation',
            options={'verbose_name_plural': 'évaluations', 'verbose_name': 'évaluation'},
        ),
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name_plural': 'questions fréquentes', 'verbose_name': 'question fréquente'},
        ),
        migrations.AlterModelOptions(
            name='faqsection',
            options={'verbose_name_plural': 'sections de la FAQ', 'verbose_name': 'section de la FAQ'},
        ),
        migrations.AlterModelOptions(
            name='inappropriate',
            options={'verbose_name_plural': 'contenus inappropriés', 'verbose_name': 'contenu inapproprié'},
        ),
        migrations.AlterModelOptions(
            name='meeting',
            options={'verbose_name_plural': 'rendez-vous', 'verbose_name': 'rendez-vous'},
        ),
        migrations.AlterModelOptions(
            name='meetingpoint',
            options={'verbose_name_plural': 'points de rencontre', 'verbose_name': 'point de rencontre'},
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name_plural': 'membres', 'verbose_name': 'membre'},
        ),
        migrations.AlterModelOptions(
            name='offer',
            options={'verbose_name_plural': 'offres', 'verbose_name': 'offre'},
        ),
        migrations.AlterModelOptions(
            name='passwordrecovery',
            options={'verbose_name_plural': 'réinitialisations de mot de passe', 'verbose_name': 'réinitialisation de mot de passe'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'profils', 'verbose_name': 'profil'},
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'verbose_name_plural': 'demandes', 'verbose_name': 'demande'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name_plural': 'compétences', 'verbose_name': 'compétence'},
        ),
        migrations.AlterModelOptions(
            name='skillcategory',
            options={'verbose_name_plural': 'catégories de compétence', 'verbose_name': 'catégorie de compétence'},
        ),
        migrations.AlterModelOptions(
            name='tos',
            options={'verbose_name_plural': 'cgu', 'verbose_name': 'cgu'},
        ),
        migrations.AddField(
            model_name='skill',
            name='title',
            field=models.CharField(default='Titre', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='mark',
            field=models.IntegerField(choices=[(4, 'Excellent'), (5, 'Perfect'), (3, 'Good'), (2, 'Neutral'), (0, 'Dangerous'), (1, 'Bad')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='P', choices=[('R', 'Refusé'), ('P', 'En attente'), ('A', 'Accepté')], max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(default='2', choices=[('0', 'Propriétaire'), ('1', 'Modérateur'), ('2', 'Membre')], max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='status',
            field=models.CharField(default='0', choices=[('0', 'En attente'), ('1', 'Accepté'), ('2', 'Banni')], max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='favorite_contact',
            field=models.CharField(default='N', choices=[('E', 'Email'), ('P', 'Téléphone'), ('N', 'Aucun')], max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='O', choices=[('M', 'Homme'), ('F', 'Femme'), ('O', 'Autre')], max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, 'Moyen'), (2, 'Elevé'), (3, 'Expert')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='category',
            field=models.CharField(default='O', choices=[('B', 'Signalement de bug'), ('U', 'Amélioration'), ('O', 'Autres')], max_length=1),
            preserve_default=True,
        ),
    ]
