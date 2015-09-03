from django.http import JsonResponse

class JsonResponsePermanentRedirect(JsonResponse):
    status_code = 301


class JsonResponseRedirect(JsonResponse):
    status_code = 302


class JsonResponseNotModified(JsonResponse):
    status_code = 304


class JsonResponseBadRequest(JsonResponse):
    status_code = 400


class JsonResponseUnauthorized(JsonResponse):
    status_code = 401


class JsonResponseForbidden(JsonResponse):
    status_code = 403


class JsonResponseNotFound(JsonResponse):
    status_code = 404


class JsonResponseNotAllowed(JsonResponse):
    status_code = 405


class JsonResponseGone(JsonResponse):
    status_code = 410


class JsonResponseServerError(JsonResponse):
    status_code = 500
