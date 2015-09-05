# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0002_auto_20150904_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='Privacidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_publico', models.BooleanField(default=True)),
                ('sexo_publico', models.BooleanField(default=True)),
                ('fecha_nacimiento_publico', models.BooleanField(default=True)),
                ('telefono_publico', models.BooleanField(default=True)),
                ('bio_publico', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='correo_publico',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='telefono_publico',
        ),
        migrations.AlterField(
            model_name='perfil',
            name='imagen',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'imagenes/perfiles', blank=True),
        ),
    ]
