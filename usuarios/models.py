# -*- coding: utf-8 -*-

import uuid

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from conecta2.utils import image_to_dataURI, slugify_path
from easy_thumbnails.fields import ThumbnailerImageField
from votos.models import Voto

class ProxyUser(User):
    class Meta:
        proxy = True

    def clean(self):
        print('cleaning')
        raise ValidationError('ERRORORORRORO')
        #print('Hola proxy!')


class Perfil(models.Model):
    SEXO_CHOICES = (('f', 'Femenino'), ('m', 'Masculino'))
    
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    bio = models.CharField(max_length=1000, blank=True)
    imagen = ThumbnailerImageField(upload_to=slugify_path('imagenes/perfiles'), blank=True)

    email_verificado = models.BooleanField(default=False)
    
    votos = GenericRelation('votos.Voto')

    def porcentaje(self):
        valores = [
            int(bool(self.usuario.email)),
            int(bool(self.usuario.first_name)),
            int(bool(self.usuario.last_name)),
            int(bool(self.sexo)),
            int(bool(self.fecha_nacimiento)),
            int(bool(self.telefono)),
            int(bool(self.bio)),
            int(bool(self.imagen)),
            int(bool(self.usuario.habilidades.all()))
        ]

        suma = sum(valores)
        return int(100 * suma / float(len(valores)))

    @property
    def nivel_actual(self):
        if not hasattr(self, '_nivel_actual'):
            self._nivel_actual = Nivel.objects.filter(horas__lte=self.horas_acumuladas).last()

        return self._nivel_actual

    @property 
    def nivel_siguiente(self):
        if not hasattr(self, '_nivel_siguiente'):
            self._nivel_siguiente = Nivel.objects.filter(horas__gt=self.horas_acumuladas).first()

        return self._nivel_siguiente

    @property
    def horas_acumuladas(self):
        if not hasattr(self, '_horas_acumuladas'):
            self._horas_acumuladas = float(sum([evento.duracion() for evento in self.usuario.eventos.filter(participacion__verificada=True).all()]))

        return self._horas_acumuladas

    def lista_habilidades(self):
        return [h.as_dict() for h in self.usuario.habilidades.all()]

    def nivel_data(self):
        return {
            'horas_acumuladas': '%sh' % str(self.horas_acumuladas)[0:str(self.horas_acumuladas).index('.') + 2],
            'nivel_actual': {
                'titulo': self.nivel_actual.titulo if self.nivel_actual else None,
                'horas': '%sh' % str(self.nivel_actual.horas) if self.nivel_actual else None,
            },
            'nivel_siguiente': {
                'horas': '%sh' % str(self.nivel_siguiente.horas) if self.nivel_siguiente is not None else None
            },
            'progreso': ((self.horas_acumuladas - float(self.nivel_actual.horas)) / (float(self.nivel_siguiente.horas) - float(self.nivel_actual.horas))) if self.nivel_siguiente is not None else float(1)
        }

    def as_dict(self, preview=False, viewer=None):
        res = {
            'id': self.usuario.id,
            'username': self.usuario.username,
            'full_name': self.usuario.get_full_name(),
            'nivel_data': self.nivel_data(),
            'votos': {
                'recibidos': self.votos.count(),
                'dados': Voto.objects.filter(usuario=self.usuario, content_type__model='perfil').count()
            }
        }

        if preview:
            if self.imagen:
                res['pictures'] = {'medium': image_to_dataURI(self.imagen['medium'])}
            else:
                res['pictures'] = {'medium': None}
        else:
            res.update({
                'email': self.usuario.email, 
                'first_name': self.usuario.first_name, 
                'last_name': self.usuario.last_name, 
                'short_name': self.usuario.get_short_name(), 
                'sexo': self.sexo,
                'fecha_nacimiento': self.fecha_nacimiento,
                'telefono': self.telefono,
                'bio': self.bio,
                'privacidad': self.usuario.privacidad.as_dict()
            })

            if self.imagen:
                res['pictures'] = {'full': image_to_dataURI(self.imagen)}
            else:
                res['pictures'] = {'full': None}

        if viewer != self.usuario:
            if not self.usuario.privacidad.email_publico:
                res.pop('email', None)

            if not self.usuario.privacidad.sexo_publico:
                res.pop('sexo', None)

            if not self.usuario.privacidad.fecha_nacimiento_publico:
                res.pop('fecha_nacimiento', None)

            if not self.usuario.privacidad.telefono_publico:
                res.pop('telefono', None)

            if not self.usuario.privacidad.bio_publico:
                res.pop('bio', None)
        else:
            res.update({'completacion': self.porcentaje()})

        res['me_llega'] = self.votos.filter(usuario=viewer).exists()

        if self.usuario.is_superuser:
            res['username'] = u'%s ✪' % res['username']

        return res

    def save(self, *args, **kwargs):
        super(Perfil, self).save(*args, **kwargs)
        
        if self.usuario and not hasattr(self.usuario, 'privacidad') or not self.usuario.privacidad:
            privacidad = Privacidad(usuario=self.usuario)
            privacidad.save()


    def __unicode__(self):
        return u'%s (%d%% complete)' % (self.usuario.get_full_name() or self.usuario, self.porcentaje())

    class Meta:
        verbose_name_plural = 'perfiles'


class Privacidad(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    email_publico = models.BooleanField(default=True)
    sexo_publico = models.BooleanField(default=True)
    fecha_nacimiento_publico = models.BooleanField(default=True)
    telefono_publico = models.BooleanField(default=True)
    bio_publico = models.BooleanField(default=True)
    recibir_notificaciones = models.BooleanField(default=True)

    def as_dict(self):
        return {
            'email_publico': self.email_publico,
            'sexo_publico': self.sexo_publico,
            'fecha_nacimiento_publico': self.fecha_nacimiento_publico,
            'telefono_publico': self.telefono_publico,
            'bio_publico': self.bio_publico,
            'recibir_notificaciones': self.recibir_notificaciones
        }

    def __unicode__(self):
        return u'%s' % (self.usuario)

    class Meta:
        verbose_name_plural = 'privacidades'


class Habilidad(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='habilidades')
    descripcion = models.CharField(max_length=500)

    def as_dict(self):
        return {'id': self.id, 'descripcion': self.descripcion}

    def __unicode__(self):
        return u'%s' % (self.descripcion)

    class Meta:
        order_with_respect_to = 'perfil'

    class Meta:
        verbose_name_plural = 'habilidades'


class Nivel(models.Model):
    titulo = models.CharField(max_length=30)
    horas = models.DecimalField(unique=True, max_digits=5, decimal_places=1, validators=[MinValueValidator(0)])
    posicion = models.PositiveSmallIntegerField(editable=False, default=0)

    def as_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'horas': self.horas,
            'posicion': self.posicion
        }

    def save(self, *args, **kwargs):
        scoot = kwargs.pop('scoot', True)
        super(Nivel, self).save(*args, **kwargs)

        if scoot:
            for i, nivel in enumerate(Nivel.objects.all(), start=1):
                nivel.posicion = i
                nivel.save(scoot=False)

    def __unicode__(self):
        return u'%d) %s - %.1f horas' % (self.posicion, self.titulo, self.horas)

    class Meta:
        verbose_name_plural = 'niveles'
        ordering = ['horas']


class VerificacionCorreo(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    codigo = models.CharField(max_length=100, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        while VerificacionCorreo.objects.filter(codigo=self.codigo).exclude(id=self.id).exists():
            self.codigo = uuid.uuid4()

        super(VerificacionCorreo, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.usuario.username