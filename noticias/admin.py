from django.contrib import admin

from .models import *

class InstitucionFilter(admin.SimpleListFilter):
    title = 'institucion'
    parameter_name = 'institucion'

    def list_uniquifier(self, seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]

    def lookups(self, request, model_admin):
        ids_instituciones = self.list_uniquifier(list(
            Noticia.objects.exclude(creador__afiliacion=None).order_by(
                '-creador__afiliacion__institucion'
            ).values_list(
                'creador__afiliacion__institucion__id',
                'creador__afiliacion__institucion__nombre'
            )
        ))

        ids_instituciones.insert(0, ('GENERAL', 'GENERAL'))
        return ids_instituciones

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        elif self.value() == 'GENERAL':
            return queryset.filter(creador__afiliacion=None)
        else:
            return queryset.filter(creador__afiliacion__institucion=self.value())


class NoticiaAdmin(admin.ModelAdmin):
    model = Noticia
    list_display = ('titulo', 'publicada', 'creador', 'institucion')
    readonly_fields = ('creador', 'vistas')
    save_on_top = True
    view_on_site = False

    def save_model(self, request, obj, form, change):
        obj.creador = request.user
        obj.save()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
                return True
            elif request.user.groups.filter(name='INST').exists() and obj is not None:
                return hasattr(request.user, 'afiliacion') and hasattr(obj.creador, 'afiliacion') and request.user.afiliacion.institucion == obj.creador.afiliacion.institucion
            
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request=request, obj=obj)

    def get_list_filter(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return (InstitucionFilter,)
        else:
            tuple()

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return Noticia.objects.all()
        elif request.user.groups.filter(name='INST').exists() and hasattr(request.user, 'afiliacion'):
            return Noticia.objects.filter(creador__afiliacion__institucion__in=[None, request.user.afiliacion.institucion])
        else:
            return []

admin.site.register(Noticia, NoticiaAdmin)