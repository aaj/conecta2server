from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.instituciones, name='instituciones'),
    url(r'/(?P<id_institucion>[0-9]+)$', views.institucion, name='institucion'),
    url(r'/(?P<id_institucion>[0-9]+)/mellega$', views.votar_institucion, name='votar_institucion')
    # URL PARA VER LOS LOGROS DE UNA INSTITUCION
    # URL PARA VER LOS RECUERDOS DE UNA INSTITUCION, AGRUPADOS POR EVENTO (PAGINADO? TOP 5?)
    # URL PARA VER LOS EVENTOS DE UNA INSTITUCION
]

# open -a Google\ Chrome --args --disable-web-security