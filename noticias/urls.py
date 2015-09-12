from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.noticias, name='noticias'),
    url(r'/(?P<id_noticia>[0-9]+)$', views.noticia, name='noticia'),
    url(r'/(?P<id_noticia>[0-9]+)/mellega$', views.votar_noticia, name='votar_noticia')
]

# open -a Google\ Chrome --args --disable-web-security