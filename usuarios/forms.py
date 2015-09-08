from django.apps import apps
from django import forms
from django.conf import settings

from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['sexo', 'fecha_nacimiento', 'telefono', 'bio', 'imagen']


class UserForm(forms.ModelForm):
    class Meta:
        model = apps.get_model(*settings.AUTH_USER_MODEL.split('.', 1))
        fields = ['username', 'first_name', 'last_name']