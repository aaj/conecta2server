from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Afiliacion

@receiver(post_save, sender=Afiliacion)
def afiliacion_creada(sender, **kwargs):
    inst_group = Group.objects.get(name='INST')
    afiliacion = kwargs['instance']
    afiliacion.usuario.groups.add(inst_group)
    afiliacion.usuario.is_staff = True
    afiliacion.usuario.save()


# @receiver(post_delete, sender=Afiliacion)
# def afiliacion_eliminada(sender, **kwargs):
#     inst_group = Group.objects.get(name='INST')
#     afiliacion = kwargs['instance']
#     afiliacion.usuario.groups.remove(inst_group)
#     if not afiliacion.usuario.is_superuser:
#         afiliacion.usuario.is_staff = False
#     afiliacion.usuario.save()