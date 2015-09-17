from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Logro

@receiver(m2m_changed, sender=Logro.usuarios.through)
def logro_asignado(sender, **kwargs):
    print("LOGRO ASIGNADO, AQUI HAY QUE HACER LA PUSH")
    print(kwargs)