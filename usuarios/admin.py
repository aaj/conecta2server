from django.contrib import admin
from usuarios.models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class PerfilInline(admin.StackedInline):
    model = Perfil

    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser:
            return tuple()
        else:
            return ('email_verificado',)


class PrivacidadInline(admin.StackedInline):
    model = Privacidad 


class HabilidadInline(admin.TabularInline):
    model = Habilidad
    extra = 1


class MyUserAdmin(UserAdmin):
    # form = MyUserChangeForm
    # fieldsets = UserAdmin.fieldsets + (
    #         (None, {'fields': ('some_extra_data',)}),
    # )

    model = User
    inlines = [PerfilInline, PrivacidadInline, HabilidadInline]

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
            return []


# admin.site.register(Perfil)
# admin.site.register(Privacidad)
# admin.site.register(Habilidad)

admin.site.register(Nivel)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
