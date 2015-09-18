from django import forms
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.core.validators import MinValueValidator

from instituciones.models import Institucion

class EventoSearchForm(forms.Form):
    institucion = forms.ModelChoiceField(required=False, queryset=Institucion.objects.all())
    fecha = forms.CharField(required=False)
    limit = forms.IntegerField(required=False, validators=[MinValueValidator(1)])
    offset = forms.IntegerField(required=False)
    tense = forms.ChoiceField(required=False, choices=(('pasados', 'Eventos Pasados'), ('futuros', 'Eventos Futuros')))

    def clean(self):
        fecha = self.cleaned_data.get('fecha')
        limit = self.cleaned_data.get('limit')
        offset = self.cleaned_data.get('offset')
        tense = self.cleaned_data.get('tense')
        
        if not fecha:
            self.cleaned_data['fecha'] = timezone.now()
        else:
            try:
                self.cleaned_data['fecha'] = parse_datetime(fecha)
            except:
                self.add_error('fecha', 'Introduzca una fecha valida.')
            else:
                if self.cleaned_data['fecha'] is None:
                    self.add_error('fecha', 'Introduzca una fecha valida.')

        if not limit:
            self.cleaned_data['limit'] = 1

        if not offset:
            self.cleaned_data['offset'] = 0
        
        if not tense:
            self.cleaned_data['tense'] = 'all'

        return self.cleaned_data