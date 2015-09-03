# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200, blank=True)),
                ('imagen', models.ImageField(upload_to=b'imagenes/noticias')),
                ('publicada', models.DateTimeField(auto_now_add=True)),
                ('vistas', models.PositiveIntegerField(default=0)),
                ('creador', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publicada'],
            },
        ),
    ]
