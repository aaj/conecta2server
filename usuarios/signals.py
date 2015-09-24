from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil

@receiver(post_save, sender=User)
def usuario_post_save(sender, **kwargs):
    print("user post save")
    usuario = kwargs['instance']

    if not hasattr(usuario, 'perfil') or not usuario.perfil:
        print("no tiene perfil")
        perfil = Perfil(usuario=usuario)
        perfil.save()
    else:
        print("si tiene perfil!")
        
    uf_group = Group.objects.get(name='UF')
    usuario.groups.add(uf_group)