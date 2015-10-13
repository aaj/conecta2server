# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .decorators import login_required_401
from .forms import *

from conecta2.http import *
from conecta2.decorators import parse_b64_files_in_body
from conecta2.utils import enviar_correo_bienvenida, enviar_correo_verificacion

from votos.utils import votar

from social.apps.django_app.utils import psa
from tokenapi.tokens import token_generator

@require_http_methods(['GET'])
def user_login(request, *args, **kwargs):
    return render(request, 'usuarios/login.html')


@psa('social:complete')
@require_http_methods(['POST'])
@csrf_exempt
def social_auth(request, backend, *args, **kwargs):
    logout(request)
    if backend == 'facebook':
        token = request.POST.get('access_token')

        try:
            user = request.backend.do_auth(token)
        except Exception as ex:
            print("do_auth exception:")
            raise ex
            print(ex)
            return JsonResponseUnauthorized({'message': 'Invalid or missing access token.'})
        else:
            if user:
                if user.is_active:
                    login(request, user)

                    return MyJsonResponse({
                        'user': user.pk, 
                        'token': token_generator.make_token(user), 
                        'perfil': user.perfil.as_dict(preview=False, viewer=user)
                    })
                else:
                    return JsonResponseUnauthorized({'message': 'Su cuenta ha sido desactivada.'})
            else:
                return JsonResponseUnauthorized({'message': 'Error de autenticacion. Intente de nuevo.'})
    else:
        return JsonResponseServerError('"%s" auth not supported.' % backend)


@require_http_methods(['POST'])
@csrf_exempt
def auth(request, *args, **kwargs):
    logout(request)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    try:
        email_validator = EmailValidator()
        email_validator(username)
        
        usuario = User.objects.filter(email__iexact=username).first()

        if usuario is not None:
            username = usuario.username
        else:
            username = ''
    except ValidationError:
        usuario = User.objects.filter(username__iexact=username).first()

        if usuario is not None:
            username = usuario.username
        else:
            username = ''

    user = authenticate(username=username, password=password)

    if user:
        if user.is_active:
            if user.perfil.email_verificado:
                login(request, user)

                return MyJsonResponse({
                    'user': user.pk, 
                    'token': token_generator.make_token(user), 
                    'perfil': user.perfil.as_dict(preview=False, viewer=user)
                })   
            else:
                return JsonResponseUnauthorized({'message': u'Tienes que verificar tu correo electrónico antes de ingresar.'})
        else:
            return JsonResponseUnauthorized({'message': 'Su cuenta ha sido desactivada.'})
    else:
        return JsonResponseUnauthorized({'message': u'Usuario o contraseña invalida.'})


@login_required_401
@require_http_methods(['GET', 'POST'])
@csrf_exempt
def mi_perfil(request, *args, **kwargs):
    return perfil(request, username=request.user.username, *args, **kwargs)


@parse_b64_files_in_body('imagen')
@login_required_401
@require_http_methods(['GET', 'POST'])
@csrf_exempt
def perfil(request, username, *args, **kwargs):
    usuario = User.objects.filter(username__iexact=username).first()

    if usuario is None:
        msg = 'Usuario %s no existe!' % username
        return JsonResponseNotFound({'message': msg})

    perfil_depurado = usuario.perfil.as_dict(preview=False, viewer=request.user)

    if request.method == 'GET':
        return MyJsonResponse({'perfil': perfil_depurado})
    else:
        if usuario == request.user:
            perfil_form = PerfilForm(request.POST, request.FILES, instance=request.user.perfil)
            user_form = UserForm(request.POST, instance=request.user)

            if perfil_form.is_valid() & user_form.is_valid():                
                perfil_form.save()
                user_form.save()

                #print(perfil_form.cleaned_data['fecha_nacimiento'].tzinfo)

                return JsonResponse({
                    'user': request.user.pk, 
                    'token': token_generator.make_token(request.user), 
                    'perfil': request.user.perfil.as_dict(viewer=request.user)
                })   
            else:
                errores = dict()
                errores.update(perfil_form.errors)
                errores.update(user_form.errors)

                return JsonResponseBadRequest(errores)
        else:
            return JsonResponseForbidden({'message': 'Usted no tiene permiso de editar este perfil.'})


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def privacidad(request, campo, *args, **kwargs):
    if campo in ['email_publico', 'sexo_publico', 'fecha_nacimiento_publico', 'telefono_publico', 'bio_publico', 'recibir_notificaciones']:
        setattr(request.user.privacidad, campo, not getattr(request.user.privacidad, campo))
        request.user.privacidad.save()
        return MyJsonResponse()
    else:
        return JsonResponseBadRequest({'message': '"%s" no es una opcion de privacidad.' % campo})


@login_required_401
@require_http_methods(['GET'])
def logros(request, username, *args, **kwargs):
    usuario = User.objects.filter(username__iexact=username).first()

    if usuario is None:
        return JsonResponseNotFound({'message': 'Usuario no existe.'})

    return MyJsonResponse([l.as_dict() for l in usuario.logros.all()], safe=False)


@login_required_401
@require_http_methods(['GET', 'POST'])
@csrf_exempt
def habilidades(request, username, *args, **kwargs):
    perfil = Perfil.objects.filter(usuario__username__iexact=username).first()

    if perfil is None:
        return JsonResponseNotFound({'message': 'Usuario no existe.'})

    if request.method == 'GET':
        return MyJsonResponse(perfil.lista_habilidades(), safe=False)
    elif request.method == 'POST':
        if perfil.usuario != request.user:
            return JsonResponseForbidden({'message': 'Usted no tiene permiso de crear esa habilidad.'})
        else:
            f = HabilidadForm(request.POST)

            if f.is_valid():
                nueva_habilidad = f.save(commit=False)
                nueva_habilidad.usuario = request.user
                nueva_habilidad.save()
                return MyJsonResponse()
            else:
                return JsonResponseBadRequest(f.errors)


@login_required_401
@require_http_methods(['PUT', 'DELETE'])
@csrf_exempt
def habilidad(request, username, id_habilidad, *args, **kwargs):
    perfil = Perfil.objects.filter(usuario__username__iexact=username).first()

    if perfil is None:
        return JsonResponseNotFound({'message': 'Usuario no existe.'})

    habilidad = Habilidad.objects.filter(id=id_habilidad).first()

    if not habilidad:
        return JsonResponseNotFound({'message': 'Habilidad no existe.'})

    if perfil.usuario != habilidad.usuario:
        return JsonResponseForbidden({'message': 'Usted no tiene permiso de editar esta habilidad.'})

    if request.method == 'PUT':
        f = HabilidadForm(request.PUT, instance=habilidad)
        if f.is_valid():
            f.save()
            return MyJsonResponse()
        else:
            return JsonResponseBadRequest(f.errors)
    elif request.method == 'DELETE':
        habilidad.delete()
        return MyJsonResponse()


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def votar_perfil(request, username, *args, **kwargs):
    perfil = Perfil.objects.filter(usuario__username__iexact=username).first()

    if perfil is None:
        return JsonResponseNotFound({'message': 'Usuario no existe!'})

    me_llega = votar(thing=perfil, usuario=request.user)
    
    return MyJsonResponse({'me_llega': me_llega})


@login_required_401
@require_http_methods(['GET'])
def voluntarios(request, *args, **kwargs):
    f = VoluntariosForm(request.GET)
    if f.is_valid():
        limit = f.cleaned_data['limit']
        offset = f.cleaned_data['offset']
        voluntarios = User.objects.filter(groups__name='UF').exclude(groups__name__in=['SA', 'INST']).all()[offset:limit + offset]
        return MyJsonResponse([v.perfil.as_dict(preview=True, viewer=request.user) for v in voluntarios], safe=False)
    else:
        return JsonResponseBadRequest(f.errors)


@login_required_401
@require_http_methods(['GET'])
def eventos(request, username, *args, **kwargs):
    perfil = Perfil.objects.filter(usuario__username__iexact=username).first()

    if perfil is None:
        return JsonResponseNotFound({'message': 'Usuario no existe!'})
    
    return MyJsonResponse([e.as_dict(preview=True, viewer=perfil.usuario) for e in perfil.usuario.eventos.all()], safe=False)


@require_http_methods(['POST'])
@csrf_exempt
def register(request, *args, **kwargs):
    f = RegisterForm(request.POST)
    if f.is_valid():
        username = f.cleaned_data['username']
        email = f.cleaned_data['email']
        password = f.cleaned_data['password']

        nuevo_usuario = User.objects.create_user(username, email, password)

        try:
            verificacion = VerificacionCorreo.objects.get(usuario=nuevo_usuario)
        except:
            verificacion = VerificacionCorreo(usuario=nuevo_usuario)
            verificacion.save()

        enviar_correo_bienvenida(request, verificacion, password)

        return MyJsonResponse()
    else:
        return JsonResponseBadRequest(f.errors)


@require_http_methods(['GET'])
def verificar_correo(request, codigo, *args, **kwargs):
    try:
        verificacion = VerificacionCorreo.objects.get(codigo=codigo)
        verificacion.usuario.perfil.email_verificado = True
        verificacion.usuario.perfil.save()
        return render(request, 'usuarios/verificar_correo.html', {'success': True})
    except Exception as ex:
        print("Error verificando correo:")
        print(ex)
        return render(request, 'usuarios/verificar_correo.html', {'success': False})


@require_http_methods(['POST'])
@csrf_exempt
def enviar_verificacion(request, *args, **kwargs):
    email = request.POST.get('email', None)

    if not email or not User.objects.filter(email=email).exists():
        return JsonResponseNotFound({'message': 'No existe un usuario con ese correo electronico.'})
    else:
        usuario = User.objects.get(email=email)

        try:
            verificacion = VerificacionCorreo.objects.get(usuario=usuario)
        except:
            verificacion = VerificacionCorreo(usuario=usuario)
            verificacion.save()

        enviar_correo_verificacion(request, verificacion)

        return MyJsonResponse()


@login_required_401
@require_http_methods(['POST'])
@csrf_exempt
def cambiar_clave(request, *args, **kwargs):
    f = CambiarClaveForm(request.POST)

    if f.is_valid():
        old = f.cleaned_data['old']
        if authenticate(username=request.user.username, password=old):
            new = f.cleaned_data['new1']
            request.user.set_password(new)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return MyJsonResponse()
        else:
            return JsonResponseBadRequest({'message': u'La contraseña es invalida.'})
    else:
        return JsonResponseBadRequest(f.errors)