from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^auth/(?P<backend>[^/]+)/$', views.social_auth, name='social_auth'),
    url(r'^auth/$', views.auth, name='auth'),
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.login, name='login'),
]