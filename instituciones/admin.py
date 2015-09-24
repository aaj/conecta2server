from django.contrib import admin
from django.contrib.auth.models import User

from .models import *

# Register your models here.

class NecesidadInline(admin.TabularInline):
    model = Necesidad
    extra = 1


class AfiliacionInline(admin.TabularInline):
    model = Afiliacion
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'usuario':
            kwargs['queryset'] = User.objects.filter(groups__name='INST')

        return super(AfiliacionInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return []
        else:
            return ['usuario', 'institucion']
        
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        return self.has_add_permission(request, obj)


class InstitucionAdmin(admin.ModelAdmin):
    inlines = [NecesidadInline, AfiliacionInline]

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return Institucion.objects.all()
        elif request.user.groups.filter(name='INST').exists() and hasattr(request.user, 'afiliacion'):
            return Institucion.objects.filter(id=request.user.afiliacion.institucion.id)
        else:
            #sospecho que esto va a suceder, pero solo va a suceder si crean un usuario UF y le dan acceso al admin via is_staff = True
            return Institucion.objects.none()


admin.site.register(Institucion, InstitucionAdmin)