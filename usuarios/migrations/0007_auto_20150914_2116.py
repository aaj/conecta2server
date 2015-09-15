# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_auto_20150912_1753'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='habilidad',
            options={'verbose_name_plural': 'habilidades'},
        ),
        migrations.AlterModelOptions(
            name='nivel',
            options={'ordering': ['horas'], 'verbose_name_plural': 'niveles'},
        ),
        migrations.AlterModelOptions(
            name='perfil',
            options={'verbose_name_plural': 'perfiles'},
        ),
        migrations.AlterModelOptions(
            name='privacidad',
            options={'verbose_name_plural': 'privacidades'},
        ),
        migrations.AlterOrderWithRespectTo(
            name='habilidad',
            order_with_respect_to=None,
        ),
    ]
