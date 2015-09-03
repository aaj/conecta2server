# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('lugar', geoposition.fields.GeopositionField(max_length=42)),
                ('direccion', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to=b'imagenes/eventos')),
                ('inicio', models.DateTimeField()),
                ('fin', models.DateTimeField()),
                ('codigo_qr', models.CharField(default=uuid.uuid4, unique=True, max_length=100)),
                ('imagen_qr', models.ImageField(upload_to=b'imagenes/eventos/qr')),
                ('vistas', models.PositiveIntegerField(default=0)),
                ('institucion', models.ForeignKey(related_name='eventos', to='instituciones.Institucion')),
            ],
            options={
                'ordering': ['-inicio'],
            },
        ),
        migrations.CreateModel(
            name='Logro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('imagen', models.ImageField(upload_to=b'imagenes/logros')),
                ('evento', models.OneToOneField(to='eventos.Evento')),
                ('usuarios', models.ManyToManyField(related_name='logros', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('verificada', models.BooleanField(default=False)),
                ('evento', models.ForeignKey(to='eventos.Evento')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recuerdo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(upload_to=b'imagenes/eventos/recuerdos')),
                ('evento', models.ForeignKey(to='eventos.Evento')),
            ],
        ),
        migrations.AddField(
            model_name='evento',
            name='participantes',
            field=models.ManyToManyField(related_name='participaciones', through='eventos.Participacion', to=settings.AUTH_USER_MODEL),
        ),
    ]
