import json
from django.http import JsonResponse
from django.http.request import QueryDict

class MyJsonResponse(JsonResponse):
    def __init__(self, data={}, **kwargs):
        super(MyJsonResponse, self).__init__(data=data, **kwargs)


class JsonResponsePermanentRedirect(MyJsonResponse):
    status_code = 301


class JsonResponseRedirect(MyJsonResponse):
    status_code = 302


class JsonResponseNotModified(MyJsonResponse):
    status_code = 304


class JsonResponseBadRequest(MyJsonResponse):
    status_code = 400


class JsonResponseUnauthorized(MyJsonResponse):
    status_code = 401


class JsonResponseForbidden(MyJsonResponse):
    status_code = 403


class JsonResponseNotFound(MyJsonResponse):
    status_code = 404


class JsonResponseNotAllowed(MyJsonResponse):
    status_code = 405


class JsonResponseGone(MyJsonResponse):
    status_code = 410


class JsonResponseServerError(MyJsonResponse):
    status_code = 500


def querydict_from_json(json_string):
    try:
        obj = json.loads(json_string)
    except ValueError:
        # print("Error parsing JSON to QueryDict: Invalid JSON.")
        return QueryDict()
    else:
        if type(obj) != dict:
            # print("Error parsing JSON to QueryDict: JSON must be a single object.")
            return QueryDict()
        else:
            qd = QueryDict(mutable=True)

            for key,value in obj.iteritems():
                qd[key] = value

            return qd