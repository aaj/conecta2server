# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_auto_20150904_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='creador',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
