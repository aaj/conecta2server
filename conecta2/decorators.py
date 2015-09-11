from functools import wraps
from conecta2.utils import parse_dataURI

from django.core.files.uploadedfile import SimpleUploadedFile

def parse_b64_files_in_body(*fieldnames):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, username, *args, **kwargs):
            print("i'm here. checking *fieldnames:")
            for fieldname in fieldnames:
                print(fieldname)
                if fieldname in request.ANY and request.ANY[fieldname]:
                    fieldvalue = request.ANY[fieldname]

                    content, content_type, extension = parse_dataURI(fieldvalue)

                    if content and content_type:
                        request.FILES[fieldname] = SimpleUploadedFile.from_dict({
                            'filename': '%s%s' % (fieldname, extension),
                            'content': content,
                            'content-type': content_type
                        })
                else:
                    qd = getattr(request, request.method).copy()
                    qd['%s-clear' % fieldname] = 'on'
                    setattr(request, request.method, qd)
                    
            return view_func(request, username, *args, **kwargs)
        return _wrapped_view
    return decorator