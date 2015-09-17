from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

from conecta2.utils import image_to_dataURI

from easy_thumbnails.fields import ThumbnailerImageField
# Create your models here.

class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    logo = ThumbnailerImageField(upload_to='imagenes/logos')
    telefono_contacto = models.CharField(max_length=12, blank=True)
    direccion_contacto = models.CharField(max_length=100, blank=True)
    correo_contacto = models.EmailField(blank=True)
    pagina = models.URLField(blank=True)

    votos = GenericRelation('votos.Voto')
    
    def as_dict(self, preview=False, viewer=None):
        res = {
            'id': self.id,
            'nombre': self.nombre,
            'logo': image_to_dataURI(self.logo['small']),
            'votos': self.votos.count(),
            'eventos': self.eventos.count(),
            'me_llega': self.votos.filter(usuario=viewer).exists()
        }
        
        if not preview:
            res.update({
                'descripcion': self.descripcion,
                'logo': image_to_dataURI(self.logo['medium']),
                'telefono_contacto': self.telefono_contacto,
                'direccion_contacto': self.direccion_contacto,
                'correo_contacto': self.correo_contacto,
                'pagina': self.pagina
            })

        return res
        
    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'instituciones'


class Necesidad(models.Model):
    institucion = models.ForeignKey('Institucion', related_name='necesidades')
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s - %s' % (self.descripcion, self.institucion.nombre)

    class Meta:
        verbose_name_plural = 'necesidades'


class Afiliacion(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    institucion = models.ForeignKey('Institucion', related_name='afiliados')

    def __unicode__(self):
        return '%s - %s' % (self.usuario, self.institucion)

    class Meta:
        verbose_name_plural = 'afiliaciones'