from django.http.request import QueryDict
from conecta2.http import querydict_from_json

class PlatformIdentificationMiddleware(object):
    def process_request(self, request):
        request.PUT = QueryDict()
        request.DELETE = QueryDict()

        if request.method in ['PUT', 'DELETE']:
            setattr(request, request.method, QueryDict(request.body))

        request.platform = request.GET.get('platform', request.POST.get('platform', request.PUT.get('platform', request.DELETE.get('platform', 'web'))))
        request.ANY = QueryDict(mutable=True)
        request.ANY.update(request.GET)
        request.ANY.update(request.POST)
        request.ANY.update(request.PUT)
        request.ANY.update(request.DELETE)