from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^login$', views.user_login, name='login'),
    
    url(r'^auth$', views.auth, name='auth'),
    url(r'^auth/(?P<backend>[^/]+)$', views.social_auth, name='social_auth'),
    
    url(r'^perfil$', views.mi_perfil, name='mi_perfil'),
    url(r'^perfil/(?P<username>[^/]+)$', views.perfil, name='perfil'),
    # url(r'^register/$', views.register, name='register'),

    url(r'^privacidad/(?P<campo>[^/]+)$', views.privacidad, name='privacidad'),
    url(r'^habilidades$', views.habilidades, name='habilidades'),
]

# open -a Google\ Chrome --args --disable-web-security