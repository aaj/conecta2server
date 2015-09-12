from django.contrib.contenttypes.models import ContentType

from .models import Voto


def votar(thing, usuario):
    content_type = ContentType.objects.get_for_model(thing)

    voto = Voto.objects.filter(content_type=content_type, object_id=thing.id, usuario=usuario).first()

    if voto is None:
        voto = Voto(content_type=content_type, object_id=thing.id, usuario=usuario)
        voto.save()
        return True
    else:
        voto.delete()
        return False
