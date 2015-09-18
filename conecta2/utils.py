import json
import imghdr
import mimetypes
import urllib2

from base64 import b64encode, b64decode, encodestring

def image_to_dataURI(imageField):
    try:
        with open(imageField.path, 'rb') as file:
            data = file.read()

        encoded = b64encode(data)
        ext = imghdr.what(imageField.path)
        mime = 'image/%s' % ext if ext else 'image'

        return 'data:%s;base64,%s' % (mime, encoded)
    except EnvironmentError as ex:
        print("Could not convert imagefield to dataUIR.")
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
        print("Bad dataURI format. Cannot extract mimetype. Using default application/octet-stream.")
        return 'application/octet-stream'


def b64content_from_dataURI(dataURI):
    try:
        start = dataURI.index('base64,') + len('base64,')
        return b64decode(dataURI[start:])
    except Exception as ex:
        print("Bad dataURI format. Cannot extract b64 content. Using default empty string.")
        print(ex)
        return ''


def send_push(post_data_dict):
    post_data_json = json.dumps(post_data_dict)
    app_id = '5cb9d9e9'
    private_key = '7c697ed2ceaa91cd68d0bfdbe8bcc3f960e090f23eb4d469'
    url = "https://push.ionic.io/api/v1/push"
    req = urllib2.Request(url, data=post_data_json)
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Ionic-Application-Id", app_id)
    b64 = encodestring('%s:' % private_key).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % b64)

    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        print('Error enviando push: ')
        print(e)
        print(e.read())
        print('Datos: ')
        print(post_data_json)