import imghdr
import mimetypes
from base64 import b64encode, b64decode

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


#data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ