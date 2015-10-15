from django.contrib import admin

from conecta2.utils import send_push_logro

from .models import *

from instituciones.models import Institucion

class LogroInline(admin.TabularInline):
    model = Logro
    fields = ('nombre', 'imagen',)

    def save_related(self, request, form, formsets, change):
        super(LogroInline, self).save_related(request, form, formsets, change)

        usuarios = lists()

        for usuario in form.instance.evento.participantes.filter(participacion__verificada=True, privacidad__recibir_notificaciones=True).all():
            if not usuario.logros.filter(id=form.instance.id).exists():
                form.instance.usuarios.add(usuario)
                usuarios.append(usuario)

        if len(usuarios) > 0:
            send_push_logro(form.instance, usuarios)


class RecuerdoInline(admin.TabularInline):
    model = Recuerdo
    extra = 1

class EventoAdmin(admin.ModelAdmin):
    model = Evento
    list_display = ('nombre', 'institucion', 'inicio', 'fin', 'votos_count', 'participantes_count', 'participantes_verificados_count', 'vistas')
    readonly_fields = ('vistas', 'codigo_qr', 'imagen_qr')
    save_on_top = True
    view_on_site = False

    inlines = [LogroInline, RecuerdoInline]

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
                return True
            elif request.user.groups.filter(name='INST').exists() and obj is not None:
                return hasattr(request.user, 'afiliacion') and obj.institucion == request.user.afiliacion.institucion
            
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request=request, obj=obj)

    def get_list_filter(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return ('institucion',)
        else:
            tuple()

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return Evento.objects.all()
        elif request.user.groups.filter(name='INST').exists() and hasattr(request.user, 'afiliacion'):
            return Evento.objects.filter(institucion=request.user.afiliacion.institucion)
        else:
            return Evento.objects.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            kwargs['queryset'] = Institucion.objects.all()
        elif request.user.groups.filter(name='INST').exists() and hasattr(request.user, 'afiliacion'):
            kwargs['queryset'] = Institucion.objects.filter(id=request.user.afiliacion.institucion.id)
            kwargs['empty_label'] = None
        else:
            kwargs['queryset'] = Car.objects.filter(owner=request.user)
        
        return super(EventoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Evento, EventoAdmin)
admin.site.register(Participacion)