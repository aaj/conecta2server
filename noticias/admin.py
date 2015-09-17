from django.contrib import admin

from .models import *

class InstitucionFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'institucion'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'institucion'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        ids_instituciones = list(
            Noticia.objects.exclude(creador__afiliacion=None).values_list(
                'creador__afiliacion__institucion__id',
                'creador__afiliacion__institucion__nombre'
            ).order_by(
                '-creador__afiliacion__institucion'
            ).distinct(
                'creador__afiliacion__institucion'
            )
        )

        ids_instituciones.insert(0, ('GENERAL', 'GENERAL'))
        return ids_instituciones

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

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