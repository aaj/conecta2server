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


class InstitucionAdmin(admin.ModelAdmin):
    inlines = [NecesidadInline, AfiliacionInline]

admin.site.register(Institucion, InstitucionAdmin)