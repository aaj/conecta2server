# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def eliminar_grupos_default(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    Group.objects.filter(name='ADMIN').delete()
    Group.objects.filter(name='INST').delete()
    Group.objects.filter(name='UF').delete()


def crear_grupos_default(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    
    if not Group.objects.filter(name='ADMIN').exists():
        admin = Group(name='ADMIN')
        admin.save()

    if not Group.objects.filter(name='INST').exists():
        inst = Group(name='INST')
        inst.save()

    if not Group.objects.filter(name='UF').exists():
        uf = Group(name='UF')
        uf.save()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_privacidad_recibir_notificaciones'),
    ]

    operations = [
        migrations.RunPython(code=crear_grupos_default, reverse_code=eliminar_grupos_default),
    ]