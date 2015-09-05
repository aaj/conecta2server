# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_auto_20150904_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='imagen',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'imagenes/eventos'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='imagen_qr',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'imagenes/eventos/qr', editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='logro',
            name='imagen',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'imagenes/logros'),
        ),
        migrations.AlterField(
            model_name='recuerdo',
            name='imagen',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'imagenes/eventos/recuerdos'),
        ),
    ]
