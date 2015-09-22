# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '0004_auto_20150914_2116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institucion',
            options={'ordering': ('nombre',), 'verbose_name_plural': 'instituciones'},
        ),
    ]
