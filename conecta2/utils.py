import json
import imghdr
import mimetypes
import urllib2

from base64 import b64encode, b64decode, encodestring

from django.db.models.query import QuerySet
from django.apps import apps

def image_to_dataURI(imageField):
    try:
        with open(imageField.path, 'rb') as file:
            data = file.read()

        encoded = b64encode(data)
        ext = imghdr.what(imageField.path)
        mime = 'image/%s' % ext if ext else 'image'

        return 'data:%s;base64,%s' % (mime, encoded)
    except EnvironmentError as ex:
        print('Could not convert imagefield to dataUIR.')
        print(ex)
        return None


def parse_dataURI(dataURI):
    content = b64content_from_dataURI(dataURI)
    content_type = mimetype_from_dataURI(dataURI)
    extension = mimetypes.guess_extension(content_type) or '.file'

    return content, content_type, extension


def mimetype_from_dataURI(dataURI):
    try:
        start = dataURI.index('data:') + len('data:')
        end = dataURI.index(';')
        return dataURI[start:end]
    except Exception as ex:
        print('Bad dataURI format. Cannot extract mimetype. Using default application/octet-stream.')
        return 'application/octet-stream'


def b64content_from_dataURI(dataURI):
    try:
        start = dataURI.index('base64,') + len('base64,')
        return b64decode(dataURI[start:])
    except Exception as ex:
        print('Bad dataURI format. Cannot extract b64 content. Using default empty string.')
        print(ex)
        return ''

def send_push(data_dict):
    data_json = json.dumps(data_dict)
    app_id = '5cb9d9e9'
    private_key = '7c697ed2ceaa91cd68d0bfdbe8bcc3f960e090f23eb4d469'
    url = 'https://push.ionic.io/api/v1/push'
    req = urllib2.Request(url, data=data_json)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Ionic-Application-Id', app_id)
    b64 = encodestring('%s:' % private_key).replace('\n', '')
    req.add_header('Authorization', 'Basic %s' % b64)
    try:
        resp = urllib2.urlopen(req)
        print(resp.read())
    except urllib2.HTTPError as e:
        print('Error enviando push: ')
        print(e)
        print(e.read())
        print('Datos: ')
        print(data_json)


def get_user_ids(users):
    User = apps.get_model(app_label='auth', model_name='User')
    if type(users) is list:
        return [str(u.id) for u in users]
    elif type(users) is QuerySet:
        return [str(i) for i in list(users.values_list('id', flat=True))]
    elif type(users) is User:
        return [str(users.id)]
    else:
        raise AssertionError('users parameter must be a list or a QuerySet.')    


def send_push_default(title, alert, users):
    send_push({
        'user_ids': get_user_ids(users),
        'production': False,
        'notification': {
            'title': title,
            'alert': alert,
            'android': {
                'payload': {
                    'type': 0
                }
            },
            'ios': {
                'payload': {
                    'type': 0
                }
            }
        }
    })


def send_push_evento(evento, users):
    send_push({
        'user_ids': get_user_ids(users),
        'production': False,
        'notification': {
            'title': 'Nuevo evento publicado',
            'alert': 'La institucion %s ha creado un nuevo evento.' % evento.institucion.nombre,
            'android': {
                'payload': {
                    'type': 1,
                    'evento': {
                        'id': evento.id,
                        'nombre': evento.nombre,
                        'institucion': {
                            'id': evento.institucion.id,
                            'nombre': evento.institucion.nombre
                        }
                    }
                }
            },
            'ios': {
                'payload': {
                    'type': 1,
                    'evento': {
                        'id': evento.id,
                        'nombre': evento.nombre,
                        'institucion': {
                            'id': evento.institucion.id,
                            'nombre': evento.institucion.nombre
                        }
                    }
                }
            }
        }
    })


def send_push_logro(logro, users):
    send_push({
        'user_ids': get_user_ids(users),
        'production': False,
        'notification': {
            'title': 'Felicidades!',
            'alert': 'Has ganado un logro!',
            'android': {
                'payload': {
                    'type': 3,
                    'logro': {
                        'id': logro.id,
                        'nombre': logro.nombre
                    }
                }
            },
            'ios': {
                'payload': {
                    'type': 3,
                    'logro': {
                        'id': logro.id,
                        'nombre': logro.nombre
                    }
                }
            }
        }
    })