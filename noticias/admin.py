from django.contrib import admin

from .models import *

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
            return ('creador__afiliacion__institucion',)
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