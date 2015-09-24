from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Noticia

from conecta2.http import *

from usuarios.decorators import login_required_401
from votos.utils import votar

@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def noticias(request, *args, **kwargs):
    try:
        limit = int(request.GET.get('limit'))
    except:
        limit = 5

    try:
        offset = int(request.GET.get('offset'))
    except:
        offset = 0

    noticias = Noticia.objects.all()[offset:limit+offset]

    return MyJsonResponse([n.as_dict(preview=True, viewer=request.user) for n in noticias], safe=False)


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def noticia(request, id_noticia, *args, **kwargs):
    noticia = Noticia.objects.filter(id=id_noticia).first()

    if noticia is None:
        return JsonResponseNotFound({'message': 'Noticia no existe!'})

    return MyJsonResponse(noticia.as_dict(preview=False, viewer=request.user))


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def votar_noticia(request, id_noticia, *args, **kwargs):
    noticia = Noticia.objects.filter(id=id_noticia).first()

    if noticia is None:
        return JsonResponseNotFound({'message': 'Noticia no existe!'})

    me_llega = votar(thing=noticia, usuario=request.user)
    
    return MyJsonResponse({'me_llega': me_llega})