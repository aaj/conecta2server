# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20150904_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='email_verificado',
            field=models.BooleanField(default=False),
        ),
    ]
