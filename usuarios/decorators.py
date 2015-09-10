from functools import wraps

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from conecta2.http import JsonResponseUnauthorized, querydict_from_json

def login_required_401(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        else:
            user = request.ANY.get('user', '')
            token = request.ANY.get('token', '')

            authed_user = authenticate(pk=user, token=token)

            if authed_user:
                login(request, authed_user)
                return f(request, *args, **kwargs)
            else:
                if request.platform == 'web':
                    return redirect(settings.LOGIN_URL)
                else:
                    return JsonResponseUnauthorized()

    return wrapper