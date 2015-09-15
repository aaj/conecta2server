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
@require_http_methods(['GET', 'POST'])
@csrf_exempt
def eventos(request, *args, **kwargs):
    if request.method == 'GET':
        print request.GET
        f = EventoSearchForm(request.GET)

        if f.is_valid():
            fecha = f.cleaned_data['fecha']
            print("LA FECHA PARA BUSCAR ES: ")
            print(fecha)
            limit = f.cleaned_data['limit']
            offset = f.cleaned_data['offset']
            tense = f.cleaned_data['tense']
            
            eventos = Evento.objects.all()

            if tense == 'pasados':
                eventos = eventos.filter(inicio__lte=fecha).order_by('-inicio')
            elif tense == 'futuros':
                eventos = eventos.filter(inicio__gte=fecha).order_by('inicio')
            
            eventos = eventos[offset:limit + offset]

            if request.platform == 'web':
                return render(request, 'eventos/list.html', {'eventos': eventos})
            else:
                return MyJsonResponse({'eventos': [e.as_dict(preview=True, viewer=request.user) for e in eventos]})
        else:
            if request.platform == 'web':
                return render(request, 'eventos/list.html', {'eventos': [], 'errores': f.errors})
            else:
                return JsonResponseBadRequest(f.errors)
    else:
        raise NotImplementedError('POST /eventos (create)')


@login_required_401
@require_http_methods(['GET', 'POST'])
@csrf_exempt
def evento(request, id_evento, *args, **kwargs):
    evento = Evento.objects.filter(id=id_evento).first()

    if evento is None:
        msg = 'Evento no existe!'

        if request.platform == 'web':
            raise Http404(msg)
        else:
            return JsonResponseNotFound({'message': msg})

    if request.method == 'GET':
        if request.platform == 'web':
            return render(request, 'eventos/detail.html', {'evento': evento})
        else:
            return MyJsonResponse({'evento': evento.as_dict(preview=False, viewer=request.user)})
    else:
        raise NotImplementedError('POST /eventos (create)')


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

    participacion = Participacion.objects.filter(evento=evento, usuario=request.user).first()

    if participacion is None:
        participacion = Participacion(evento=evento, usuario=request.user, verificada=True)
    else:
        participacion.verificada = True
    
    participacion.save()

    return MyJsonResponse(evento.participacion(usuario=request.user))
