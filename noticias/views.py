from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Noticia

from conecta2.http import *

from usuarios.decorators import login_required_401
from votos.utils import votar

def noticias(request, *args, **kwargs):
    raise NotImplementedError()


def noticia(request, *args, **kwargs):
    raise NotImplementedError()


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def votar_noticia(request, id_noticia, *args, **kwargs):
    noticia = Noticia.objects.filter(id=id_noticia).first()

    if noticia is None:
        return JsonResponseNotFound({'message': 'Noticia no existe!'})

    me_llega = votar(thing=noticia, usuario=request.user)
    
    return MyJsonResponse({'me_llega': me_llega})