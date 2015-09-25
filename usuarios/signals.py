from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil

@receiver(post_save, sender=User)
def usuario_post_save(sender, **kwargs):
    usuario = kwargs['instance']

    if not hasattr(usuario, 'perfil') or not usuario.perfil:
        perfil = Perfil(usuario=usuario)
        perfil.save()
        
    uf_group = Group.objects.get(name='UF')
    usuario.groups.add(uf_group)