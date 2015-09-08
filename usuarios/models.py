from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from conecta2.utils import dataURI
from easy_thumbnails.fields import ThumbnailerImageField
from votos.models import Voto

class Perfil(models.Model):
    SEXO_CHOICES = (('f', 'Femenino'), ('m', 'Masculino'))
    
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    bio = models.CharField(max_length=1000, blank=True)
    imagen = ThumbnailerImageField(upload_to='imagenes/perfiles', blank=True)

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
            int(bool(self.habilidades.all()))
        ]

        suma = sum(valores)
        return int(100 * suma / float(len(valores)))

    @property
    def nivel(self):
        if not hasattr(self, '_nivel'):
            self._nivel = Nivel.objects.filter(horas__lte=self.horas_acumuladas).last()

        return self._nivel

    @property 
    def siguiente_nivel(self):
        if not hasattr(self, '_siguiente_nivel'):
            self._siguiente_nivel = Nivel.objects.filter(horas__gt=self.horas_acumuladas).first()

        return self._siguiente_nivel

    @property
    def horas_acumuladas(self):
        if not hasattr(self, '_horas_acumuladas'):
            self._horas_acumuladas = sum([evento.duracion() for evento in self.usuario.eventos.all()])
        
        return self._horas_acumuladas

    @property
    def horas_para_nivelar(self):
        if not hasattr(self, '_horas_para_nivelar'):
            siguiente_nivel = Nivel.objects.filter(horas__gt=self.horas_acumuladas).first()
            self._horas_para_nivelar = siguiente_nivel.horas - self.horas_acumuladas if siguiente_nivel else 0

        return self._horas_para_nivelar

    def as_dict(self):
        res = {
            'id': self.usuario.id, 
            'username': self.usuario.username, 
            'email': self.usuario.email, 
            'first_name': self.usuario.first_name, 
            'last_name': self.usuario.last_name, 
            'short_name': self.usuario.get_short_name(), 
            'full_name': self.usuario.get_full_name(), 
            'sexo': self.sexo,
            'fecha_nacimiento': self.fecha_nacimiento,
            'telefono': self.telefono,
            'bio': self.bio,
            'privacidad': self.usuario.privacidad.as_dict(),
            'votos': {
                'recibidos': self.votos.count(),
                'dados': Voto.objects.filter(usuario=self.usuario, content_type__model='perfil').count()
            }
        }

        if self.imagen:
            res['pictures'] = {'medium': dataURI(self.imagen['medium']), 'full': dataURI(self.imagen)}
        else:
            res['pictures'] = {'medium': None, 'full': None}

        return res

    def save(self, *args, **kwargs):
        super(Perfil, self).save(*args, **kwargs)
        
        if self.usuario and not hasattr(self.usuario, 'privacidad') or not self.usuario.privacidad:
            privacidad = Privacidad(usuario=self.usuario)
            privacidad.save()


    def __unicode__(self):
        return '%s (%d%% complete)' % (self.usuario.get_full_name() or self.usuario, self.porcentaje())


class Privacidad(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    email_publico = models.BooleanField(default=True)
    sexo_publico = models.BooleanField(default=True)
    fecha_nacimiento_publico = models.BooleanField(default=True)
    telefono_publico = models.BooleanField(default=True)
    bio_publico = models.BooleanField(default=True)

    def as_dict(self):
        return {
            'email_publico': self.email_publico,
            'sexo_publico': self.sexo_publico,
            'fecha_nacimiento_publico': self.fecha_nacimiento_publico,
            'telefono_publico': self.telefono_publico,
            'bio_publico': self.bio_publico
        }

    def __unicode__(self):
        return '%s - Privacy Settings' % (self.usuario)


class Habilidad(models.Model):
    perfil = models.ForeignKey('Perfil', related_name='habilidades')
    descripcion = models.CharField(max_length=500)

    class Meta:
        order_with_respect_to = 'perfil'


class Nivel(models.Model):
    titulo = models.CharField(max_length=30)
    horas = models.PositiveSmallIntegerField(unique=True)
    posicion = models.PositiveSmallIntegerField(editable=False, default=0)


    def save(self, *args, **kwargs):
        scoot = kwargs.pop('scoot', True)
        super(Nivel, self).save(*args, **kwargs)

        if scoot:
            for i, nivel in enumerate(Nivel.objects.all(), start=1):
                nivel.posicion = i
                nivel.save(scoot=False)

    def __unicode__(self):
        return '%d) %s - %d horas' % (self.posicion, self.titulo, self.horas)

    class Meta:
        ordering = ['horas']