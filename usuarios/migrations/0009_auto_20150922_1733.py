# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_auto_20150914_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nivel',
            name='horas',
            field=models.DecimalField(unique=True, max_digits=5, decimal_places=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
