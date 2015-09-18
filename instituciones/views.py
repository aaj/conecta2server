from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Institucion

from conecta2.http import *

from usuarios.decorators import login_required_401
from votos.utils import votar
from eventos.models import Logro, Recuerdo
from eventos.views import eventos as eventos_eventos

@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def instituciones(request, *args, **kwargs):
    try:
        limit = int(request.GET.get('limit'))
    except:
        limit = 10

    try:
        offset = int(request.GET.get('offset'))
    except:
        offset = 0
    
    return MyJsonResponse([i.as_dict(preview=True, viewer=request.user) for i in Institucion.objects.all()[offset:limit + offset]], safe=False)


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def institucion(request, id_institucion, *args, **kwargs):
    institucion = Institucion.objects.filter(id=id_institucion).first()

    if institucion is None:
        return JsonResponseNotFound({'message': 'Institucion no existe!'})

    return MyJsonResponse(institucion.as_dict(preview=False, viewer=request.user))


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def votar_institucion(request, id_institucion, *args, **kwargs):
    institucion = Institucion.objects.filter(id=id_institucion).first()

    if institucion is None:
        return JsonResponseNotFound({'message': 'Institucion no existe!'})

    me_llega = votar(thing=institucion, usuario=request.user)
    
    return MyJsonResponse({'me_llega': me_llega})


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def logros(request, id_institucion, *args, **kwargs):
    institucion = Institucion.objects.filter(id=id_institucion).first()

    if institucion is None:
        return JsonResponseNotFound({'message': 'Institucion no existe.'})

    logros = Logro.objects.filter(evento__institucion=institucion).all()

    return MyJsonResponse([l.as_dict() for l in logros], safe=False)


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def eventos(request, id_institucion, *args, **kwargs):
    institucion = Institucion.objects.filter(id=id_institucion).first()

    if institucion is None:
        return JsonResponseNotFound({'message': 'Institucion no existe.'})

    request.GET = request.GET.copy() # hacerle una copia al querydict, para meterle mas datos. esto es un hack feo, no me jodas fiero
    request.GET['institucion'] = institucion.id

    return eventos_eventos(request, *args, **kwargs)


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def recuerdos(request, id_institucion, *args, **kwargs):
    institucion = Institucion.objects.filter(id=id_institucion).first()

    if institucion is None:
        return JsonResponseNotFound({'message': 'Institucion no existe.'})

    recuerdos = Recuerdo.objects.filter(evento__institucion=institucion).order_by('?')[:20]
    
    return MyJsonResponse([r.as_dict(preview=True) for r in recuerdos], safe=False)