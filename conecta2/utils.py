import imghdr
from base64 import b64encode

def dataURI(imageField):
    try:
        with open(imageField.path, 'rb') as file:
            data = file.read()

        encoded = b64encode(data)
        ext = imghdr.what(imageField.path)
        mime = 'image/%s' % ext if ext else 'image'

        return 'data:%s;base64,%s' % (mime, encoded)
    except EnvironmentError as ex:
        print(ex)
        return None