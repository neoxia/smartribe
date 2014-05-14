# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20140514_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('gender', models.CharField(default='O', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
