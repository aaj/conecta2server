from django import forms
from django.utils import timezone
from django.core.validators import MinValueValidator

class EventoSearchForm(forms.Form):
    fecha = forms.DateTimeField(required=False)
    limit = forms.IntegerField(required=False, validators=[MinValueValidator(1)])
    offset = forms.IntegerField(required=False)
    tense = forms.ChoiceField(required=False, choices=(('pasados', 'Eventos Pasados'), ('futuros', 'Eventos Futuros')))

    def clean(self):
        fecha = self.cleaned_data['fecha']
        limit = self.cleaned_data['limit']
        offset = self.cleaned_data['offset']
        tense = self.cleaned_data['tense']

        if not fecha:
            self.cleaned_data['fecha'] = timezone.now()

        if not limit:
            self.cleaned_data['limit'] = 1

        if not offset:
            self.cleaned_data['offset'] = 0
        
        if not tense:
            self.cleaned_data['tense'] = 'all'

        return self.cleaned_data


class EventoForm(forms.Form):
    pass