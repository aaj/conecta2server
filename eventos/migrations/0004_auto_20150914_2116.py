# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_auto_20150904_1928'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participacion',
            options={'verbose_name_plural': 'participaciones'},
        ),
        migrations.AlterUniqueTogether(
            name='participacion',
            unique_together=set([('evento', 'usuario')]),
        ),
    ]
