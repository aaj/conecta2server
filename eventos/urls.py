from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.eventos, name='eventos'),
    url(r'/(?P<id_evento>[0-9]+)$', views.evento, name='evento'),
    url(r'/(?P<id_evento>[0-9]+)/mellega$', views.votar_evento, name='votar_evento')
]

# open -a Google\ Chrome --args --disable-web-security