# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institucion',
            name='logo',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'imagenes/logos'),
        ),
    ]
