# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_auto_20150914_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='participantes',
            field=models.ManyToManyField(related_name='eventos', through='eventos.Participacion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recuerdo',
            name='evento',
            field=models.ForeignKey(related_name='recuerdos', to='eventos.Evento'),
        ),
    ]
