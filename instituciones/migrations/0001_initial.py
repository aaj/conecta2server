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
            name='Afiliacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('logo', models.ImageField(upload_to=b'imagenes/logos')),
                ('telefono_contacto', models.CharField(max_length=12, blank=True)),
                ('direccion_contacto', models.CharField(max_length=100, blank=True)),
                ('correo_contacto', models.EmailField(max_length=254, blank=True)),
                ('pagina', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Necesidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100)),
                ('institucion', models.ForeignKey(related_name='necesidades', to='instituciones.Institucion')),
            ],
        ),
        migrations.AddField(
            model_name='afiliacion',
            name='institucion',
            field=models.ForeignKey(related_name='afiliaciones', to='instituciones.Institucion'),
        ),
        migrations.AddField(
            model_name='afiliacion',
            name='usuario',
            field=models.ForeignKey(related_name='afiliaciones', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
