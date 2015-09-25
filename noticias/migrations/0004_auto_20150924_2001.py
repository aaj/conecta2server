# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0003_auto_20150914_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='descripcion',
            field=models.TextField(max_length=200, blank=True),
        ),
    ]
