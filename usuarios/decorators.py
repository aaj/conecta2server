from functools import wraps

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from conecta2.http import JsonResponseUnauthorized

def login_required_401(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        else:
            user = request.POST.get('user', request.GET.get('user', ''))
            token = request.POST.get('token', request.GET.get('token', ''))

            authed_user = authenticate(pk=user, token=token)

            if authed_user:
                login(request, authed_user)
                return f(request, *args, **kwargs)
            else:
                platform = request.POST.get('platform', request.GET.get('platform', 'web'))
                
                if platform == 'web':
                    return redirect(settings.LOGIN_URL)
                else:
                    return JsonResponseUnauthorized()

    return wrapper