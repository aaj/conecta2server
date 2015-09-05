# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='avatar',
            field=models.ImageField(upload_to=b'imagenes/perfiles/avatars', editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='imagen',
            field=models.ImageField(upload_to=b'imagenes/perfiles', blank=True),
        ),
    ]
