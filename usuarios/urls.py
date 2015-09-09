from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^login$', views.user_login, name='login'),
    
    url(r'^auth$', views.auth, name='auth'),
    url(r'^auth/(?P<backend>[^/]+)$', views.social_auth, name='social_auth'),
    
    url(r'^perfil$', views.perfil, name='perfil'),
    # url(r'^register/$', views.register, name='register'),
]

# open -a Google\ Chrome --args --disable-web-security