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
    
    def as_dict(self, preview=False):
        res = {
            'id': self.id,
            'nombre': self.nombre,
            'logo': image_to_dataURI(self.logo['small'])
        }
        
        if not preview:
            res.update({
                'descripcion': self.descripcion,
                'logo': image_to_dataURI(self.logo['medium']),
                'telefono_contacto': self.telefono_contacto,
                'direccion_contacto': self.direccion_contacto,
                'correo_contacto': self.correo_contacto,
                'pagina': self.pagina,
                'votos': self.votos.count()
            })

        return res
        
    def __unicode__(self):
        return self.nombre


class Necesidad(models.Model):
    institucion = models.ForeignKey('Institucion', related_name='necesidades')
    descripcion = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s - %s' % (self.descripcion, self.institucion.nombre)


class Afiliacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='afiliaciones', unique=True)
    institucion = models.ForeignKey('Institucion', related_name='afiliaciones')

    def __unicode__(self):
        return '%s - %s' % (self.usuario, self.institucion)