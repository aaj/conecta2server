from django.contrib import admin
from .models import *

class LogroAdmin(admin.ModelAdmin):
    model = Logro

    def save_related(self, request, form, formsets, change):
        super(LogroAdmin, self).save_related(request, form, formsets, change)

        for usuario in form.instance.evento.participantes.filter(participacion__verificada=True).all():
            if not usuario.logros.filter(id=form.instance.id).exists():
                form.instance.usuarios.add(usuario)


class EventoAdmin(admin.ModelAdmin):
    model = Evento
    list_display = ('nombre', 'inicio', 'fin')

admin.site.register(Evento, EventoAdmin)
admin.site.register(Logro, LogroAdmin)
admin.site.register(Participacion)