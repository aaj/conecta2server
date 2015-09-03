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
            name='Habilidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=30)),
                ('horas', models.PositiveSmallIntegerField(unique=True)),
                ('posicion', models.PositiveSmallIntegerField(default=0, editable=False)),
            ],
            options={
                'ordering': ['horas'],
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sexo', models.CharField(blank=True, max_length=10, choices=[(b'f', b'Femenino'), (b'm', b'Masculino')])),
                ('fecha_nacimiento', models.DateField(null=True, blank=True)),
                ('telefono', models.CharField(max_length=20, blank=True)),
                ('bio', models.CharField(max_length=1000, blank=True)),
                ('correo_publico', models.BooleanField(default=True)),
                ('telefono_publico', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='habilidad',
            name='perfil',
            field=models.ForeignKey(related_name='habilidades', to='usuarios.Perfil'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='habilidad',
            order_with_respect_to='perfil',
        ),
    ]
