from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Institucion

from conecta2.http import *

from usuarios.decorators import login_required_401
from votos.utils import votar

def instituciones(request, *args, **kwargs):
    raise NotImplementedError()


def institucion(request, *args, **kwargs):
    raise NotImplementedError()


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def votar_institucion(request, id_institucion, *args, **kwargs):
    institucion = Institucion.objects.filter(id=id_institucion).first()

    if institucion is None:
        return JsonResponseNotFound({'message': 'Institucion no existe!'})

    me_llega = votar(thing=institucion, usuario=request.user)
    
    return MyJsonResponse({'me_llega': me_llega})