# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_perfil_email_verificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='privacidad',
            name='recibir_notificaciones',
            field=models.BooleanField(default=True),
        ),
    ]
