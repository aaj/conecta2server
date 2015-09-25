# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_auto_20150922_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='descripcion',
            field=models.TextField(),
        ),
    ]
