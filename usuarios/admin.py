from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from usuarios.models import *

class PerfilInline(admin.StackedInline):
    model = Perfil

    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return tuple()
        else:
            return ('email_verificado',)


class PrivacidadInline(admin.StackedInline):
    model = Privacidad 


class HabilidadInline(admin.TabularInline):
    model = Habilidad
    extra = 1


class InstitucionFilter(admin.SimpleListFilter):
    title = 'institucion'
    parameter_name = 'institucion'

    def list_uniquifier(self, seq):
        seen = set()
        seen_add = seen.add
        return [ x for x in seq if not (x in seen or seen_add(x))]

    def lookups(self, request, model_admin):
        ids_instituciones = self.list_uniquifier(list(
            User.objects.exclude(afiliacion=None).all().order_by(
                'afiliacion__institucion'
            ).values_list(
                'afiliacion__institucion__id',
                'afiliacion__institucion__nombre'
            )
        ))

        ids_instituciones.insert(0, ('NINGUNA', 'NINGUNA'))
        return ids_instituciones

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        elif self.value() == 'NINGUNA':
            return queryset.filter(afiliacion=None)
        else:
            return queryset.filter(afiliacion__institucion=self.value())


class MyUserAdmin(UserAdmin):
    model = User
    inlines = [PerfilInline, PrivacidadInline, HabilidadInline]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        else:
            if request.user.is_superuser:
                return self.fieldsets #usar la configuracion default, osea mostrar TODOs los campos habidos y por haber
            else:
                return (
                    (
                        None, 
                        {
                            'fields': (
                                'username', 
                                'password'
                            )
                        }
                    ),
                    
                    (
                        _('Personal info'), 
                        {
                            'fields': (
                                'first_name', 
                                'last_name', 
                                'email'
                            )
                        }
                    ),
                    
                    (
                        _('Permissions'), 
                        {
                            'fields': (
                                'is_active', 
                                'is_staff',
                                'groups'
                            )
                        }
                    ),
                )

    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return tuple()
        else:
            return ('is_active', 'is_staff', 'groups')

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        else:
            if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
                return True
            elif request.user.groups.filter(name='INST').exists():
                return request.user == obj
            
    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request=request, obj=obj)

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return User.objects.all()
        elif request.user.groups.filter(name='INST').exists():
            return User.objects.filter(id=request.user.id)
        else:
            #sospecho que esto va a fallar, pero solo va a suceder si crean un usuario UF y le dan acceso al admin via is_staff = True
            return []

    def get_list_filter(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='SA').exists():
            return self.list_filter + (InstitucionFilter,)
        else:
            tuple()

# admin.site.register(Perfil)
# admin.site.register(Privacidad)
# admin.site.register(Habilidad)

admin.site.register(Nivel)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
