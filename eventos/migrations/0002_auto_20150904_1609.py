# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='imagen_qr',
            field=models.ImageField(upload_to=b'imagenes/eventos/qr', editable=False, blank=True),
        ),
    ]
