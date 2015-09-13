from django.apps import apps
from django import forms
from django.conf import settings
from django.core.validators import MinValueValidator

from .models import *

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['sexo', 'fecha_nacimiento', 'telefono', 'bio', 'imagen']


class UserForm(forms.ModelForm):
    class Meta:
        model = apps.get_model(*settings.AUTH_USER_MODEL.split('.', 1))
        fields = ['username', 'first_name', 'last_name']


class HabilidadForm(forms.ModelForm):
    class Meta:
        model = Habilidad
        fields = ['descripcion']


class VoluntariosForm(forms.Form):
    limit = forms.IntegerField(required=False, validators=[MinValueValidator(1)])
    offset = forms.IntegerField(required=False)
    
    def clean(self):
        limit = self.cleaned_data.get('limit')
        offset = self.cleaned_data.get('offset')
        
        if not limit:
            self.cleaned_data['limit'] = 1

        if not offset:
            self.cleaned_data['offset'] = 0
        
        return self.cleaned_data