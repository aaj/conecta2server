from datetime import timedelta

from django.http import *
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import *
from .forms import *

from conecta2.http import *

from usuarios.decorators import login_required_401
from votos.models import Voto 
from votos.utils import votar


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def eventos(request, *args, **kwargs):
    f = EventoSearchForm(request.GET)

    if f.is_valid():
        institucion = f.cleaned_data['institucion']
        fecha = f.cleaned_data['fecha']
        limit = f.cleaned_data['limit']
        offset = f.cleaned_data['offset']
        tense = f.cleaned_data['tense']

        eventos = Evento.objects.all()

        if institucion is not None:
            eventos = eventos.filter(institucion=institucion)

        if tense == 'pasados':
            eventos = eventos.filter(inicio__lte=fecha).order_by('-inicio')
        elif tense == 'futuros':
            eventos = eventos.filter(inicio__gte=fecha).order_by('inicio')
        else: # tense == 'all':
            pass # no filter. traer todo.

        eventos = eventos[offset:limit + offset]

        return MyJsonResponse({'eventos': [e.as_dict(preview=True, viewer=request.user) for e in eventos]})
    else:
        return JsonResponseBadRequest(f.errors)


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def evento(request, id_evento, *args, **kwargs):
    evento = Evento.objects.filter(id=id_evento).first()

    if evento is None:
        return JsonResponseNotFound({'message': 'Evento no existe!'})

    evento.vistas += 1
    evento.save()

    return MyJsonResponse({'evento': evento.as_dict(preview=False, viewer=request.user)})
    

@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def votar_evento(request, id_evento, *args, **kwargs):
    evento = Evento.objects.filter(id=id_evento).first()

    if evento is None:
        return JsonResponseNotFound({'message': 'Evento no existe!'})

    me_llega = votar(thing=evento, usuario=request.user)

    return MyJsonResponse({'me_llega': me_llega})


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def participar(request, id_evento, *args, **kwargs):
    evento = Evento.objects.filter(id=id_evento).first()

    if evento is None:
        return JsonResponseNotFound({'message': 'Evento no existe!'})

    participacion = Participacion.objects.filter(evento=evento, usuario=request.user).first()

    if participacion is None:
        participacion = Participacion(evento=evento, usuario=request.user, verificada=False)
        participacion.save()
    else:
        if not participacion.verificada:
            participacion.delete()
    
    return MyJsonResponse(evento.participacion(usuario=request.user))


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def verificar(request, codigo, *args, **kwargs):
    evento = Evento.objects.filter(codigo_qr=codigo).first()

    if evento is None:
        return JsonResponseNotFound({'message': 'Evento con ese codigo no existe!'})

    if timezone.now() > evento.fin:
        return JsonResponseForbidden({'message': 'Este evento ya finalizo.'})

    if timezone.now() < (evento.inicio - timedelta(hours=6)):
        return JsonResponseForbidden({'message': 'Este evento no ha comenzado.'})

    participacion = Participacion.objects.filter(evento=evento, usuario=request.user).first()

    if participacion is None:
        participacion = Participacion(evento=evento, usuario=request.user, verificada=True)
    else:
        participacion.verificada = True
    
    participacion.save()

    return MyJsonResponse(evento.as_dict(preview=False, viewer=request.user))


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def recuerdos(request, id_evento, *args, **kwargs):
    evento = Evento.objects.filter(id=id_evento).first()

    if evento is None:
        return JsonResponseNotFound({'message': 'Evento no existe!'})

    try:
        limit = int(request.GET.get('limit'))
    except:
        limit = 3

    try:
        offset = int(request.GET.get('offset'))
    except:
        offset = 0

    recuerdos = Recuerdo.objects.filter(evento=evento)[offset:limit+offset]

    return MyJsonResponse([r.as_dict(preview=True) for r in recuerdos], safe=False)


@login_required_401
@require_http_methods(['GET'])
@csrf_exempt
def recuerdo(request, id_evento, id_recuerdo, *args, **kwargs):
    recuerdo = Recuerdo.objects.filter(id=id_recuerdo, evento__id=id_evento).first()

    if recuerdo is None:
        return JsonResponseNotFound({'message': 'Recuerdo no existe!'})

    return MyJsonResponse(recuerdo.as_dict(preview=False))


def test(request, *args, **kwargs):
    if request.GET.get('a', None) == '1':
        raise Exception('Testing auto email on 500 status.')
    else:
        return HttpResponse('OK')
