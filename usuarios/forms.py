# -*- coding: utf-8 -*-

from django.apps import apps
from django import forms
from django.conf import settings
from django.core.validators import MinValueValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _

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


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username__iexact=data).exists():
            raise forms.ValidationError("Ya existe un usuario con ese nombre de usuario.")

        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email__iexact=data).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo electronico.")

        return data


class MyUserChangeForm(UserChangeForm):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def clean_username(self):
        data = self.cleaned_data['username']
        print('guardando %s' % data)
        if User.objects.filter(username__iexact=data).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ya existe un usuario con ese nombre de usuario.")

        return data

    def clean_email(self, *args, **kwargs):
        data = self.cleaned_data['email']
        if User.objects.filter(email__iexact=data).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo electronico.")

        return data


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username__iexact=data).exists():
            raise forms.ValidationError("Ya existe un usuario con ese nombre de usuario.")

        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email__iexact=data).exists():
            raise forms.ValidationError("Ya existe un usuario con ese correo electronico.")

        return data


class CambiarClaveForm(forms.Form):
    old = forms.CharField()
    new1 = forms.CharField()
    new2 = forms.CharField()

    def clean(self):
        new1 = self.cleaned_data.get('new1')
        new2 = self.cleaned_data.get('new2')
        
        if new1 and new2:
            if new1 != new2:
                raise forms.ValidationError(u'Las contraseñas no son iguales.')

        return self.cleaned_data