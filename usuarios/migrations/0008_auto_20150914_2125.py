# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0007_auto_20150914_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habilidad',
            name='perfil',
        ),
        migrations.AddField(
            model_name='habilidad',
            name='usuario',
            field=models.ForeignKey(related_name='habilidades', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
