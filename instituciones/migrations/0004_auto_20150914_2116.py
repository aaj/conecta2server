# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '0003_auto_20150912_1721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='afiliacion',
            options={'verbose_name_plural': 'afiliaciones'},
        ),
        migrations.AlterModelOptions(
            name='institucion',
            options={'verbose_name_plural': 'instituciones'},
        ),
        migrations.AlterModelOptions(
            name='necesidad',
            options={'verbose_name_plural': 'necesidades'},
        ),
    ]
