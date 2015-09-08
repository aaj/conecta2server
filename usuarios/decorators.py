from functools import wraps

from django.conf import settings
from django.shortcuts import redirect

from conecta2.http import JsonResponseUnauthorized

def login_required_401(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return JsonResponseUnauthorized()
            else:
                return redirect(settings.LOGIN_URL)

    return wrapper