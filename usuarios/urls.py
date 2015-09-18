from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^/login$', views.user_login, name='login'),
    
    url(r'^/auth$', views.auth, name='auth'),
    url(r'^/auth/(?P<backend>[^/]+)$', views.social_auth, name='social_auth'),
    
    url(r'^/perfil$', views.mi_perfil, name='mi_perfil'),
    url(r'^/perfil/(?P<username>[^/]+)$', views.perfil, name='perfil'),
    url(r'^/perfil/(?P<username>[^/]+)/logros$', views.logros, name='perfil'),
    url(r'^/perfil/(?P<username>[^/]+)/habilidades$', views.habilidades, name='perfil'),
    url(r'^/perfil/(?P<username>[^/]+)/habilidades/(?P<id_habilidad>[0-9]+)$', views.habilidad, name='perfil'),
    url(r'^/perfil/(?P<username>[^/]+)/mellega$', views.votar_perfil, name='votar_perfil'),
    # url(r'^register/$', views.register, name='register'),
    url(r'^/privacidad/(?P<campo>[^/]+)$', views.privacidad, name='privacidad'),
    url(r'^/voluntarios$', views.voluntarios, name='voluntarios')
]