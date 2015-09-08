# coding: utf-8

import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from conecta2.http import *
from .decorators import login_required_401
from .forms import *

from social.apps.django_app.utils import psa

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
            print(ex)
            return JsonResponseBadRequest({'message': 'Invalid or missing access token.'})
        else:
            if user:
                if user.is_active:
                    if user.perfil.email_verificado:
                        login(request, user)
                        return JsonResponse({'sessionid': request.session.session_key, 'csrftoken': get_token(request), 'usuario': user.perfil.as_dict()})
                    else:
                        return JsonResponseUnauthorized({'message': 'Tienes que verificar tu correo electronico antes de ingresar.'})
                else:
                    return JsonResponseUnauthorized({'message': 'Su cuenta ha sido desactivada.'})
            else:
                return JsonResponseBadRequest({'message': 'Error de autenticacion. Intente de nuevo.'})
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
        
        usuario = User.objects.filter(email=username).first()

        if usuario is not None:
            username = usuario.username
        else:
            username = ''
    except ValidationError:
        # no es un email. talvez es un username normal
        pass

    user = authenticate(username=username, password=password)

    if user:
        if user.is_active:
            if user.perfil.email_verificado:
                login(request, user)        
                return JsonResponse({'sessionid': request.session.session_key, 'csrftoken': get_token(request), 'usuario': user.perfil.as_dict()})
            else:
                return JsonResponseUnauthorized({'message': 'Tienes que verificar tu correo electronico antes de ingresar.'})
        else:
            return JsonResponseUnauthorized({'message': 'Su cuenta ha sido desactivada.'})
    else:
        return JsonResponseBadRequest({'message': u'Usuario o contraseña invalida.'})


@login_required_401
@require_http_methods(['GET', 'POST'])
def perfil(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'usuarios/perfil.html')
    else:
        perfil_form = PerfilForm(request.POST, instance=request.user.perfil)
        user_form = UserForm(request.POST, instance=request.user)

        if perfil_form.is_valid() & user_form.is_valid():
            perfil_form.save()
            user_form.save()
            return MyJsonResponse({'sessionid': request.session.session_key, 'csrftoken': get_token(request), 'usuario': user.perfil.as_dict()})
        else:
            errores = dict()
            errores.update(perfil_form.errors)
            errores.update(user_form.errors)
            
            print(errores)
            return JsonResponseBadRequest(data=errores)

# @require_http_methods(['GET', 'POST'])
# def register(request, *args, **kwargs):
#     if request.method == 'GET':
#         return HttpResponse('Aqui va la pagina de register!')
#     else: #request = POST
