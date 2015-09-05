import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token

from conecta2.http import *

from social.apps.django_app.utils import psa

@psa('social:complete')
@require_http_methods(['POST'])
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
                login(request, user)
                return JsonResponse({'sessionid': request.session.session_key, 'csrftoken': get_token(request), 'usuario': user.perfil.as_dict()})
            else:
                return JsonResponseBadRequest({'message': 'FB Login Error.'})
    else:
        return JsonResponseServerError('"%s" auth not supported.' % backend)


@require_http_methods(['POST'])
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

    if user and user.is_active:
        login(request, user)        
        return JsonResponse({'sessionid': request.session.session_key, 'csrftoken': get_token(request), 'usuario': user.perfil.as_dict()})
    else:
        return JsonResponseBadRequest({'message': 'Wrong username or password.'})


# @require_http_methods(['GET', 'POST'])
# def register(request, *args, **kwargs):
#     if request.method == 'GET':
#         return HttpResponse('Aqui va la pagina de register!')
#     else: #request = POST
