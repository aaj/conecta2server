from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.eventos, name='eventos'),
    url(r'^/(?P<id_evento>[0-9]+)$', views.evento, name='evento'),
    url(r'^/(?P<id_evento>[0-9]+)/mellega$', views.votar_evento, name='votar_evento'),
    url(r'^/(?P<id_evento>[0-9]+)/participar$', views.participar, name='participar'),
    url(r'^/(?P<id_evento>[0-9]+)/recuerdos$', views.recuerdos, name='recuerdos'),
    url(r'^/(?P<id_evento>[0-9]+)/recuerdos/(?P<id_recuerdo>[0-9]+)$', views.recuerdo, name='recuerdo'),
    url(r'^/verificar/(?P<codigo>.+)$', views.verificar, name='verificar'),
    url(r'^/test$', views.test, name='test')
]

# open -a Google\ Chrome --args --disable-web-security