# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '0002_auto_20150904_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afiliacion',
            name='institucion',
            field=models.ForeignKey(related_name='afiliados', to='instituciones.Institucion'),
        ),
        migrations.AlterField(
            model_name='afiliacion',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
