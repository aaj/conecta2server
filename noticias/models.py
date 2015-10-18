# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from conecta2.utils import image_to_dataURI, send_push_noticia, slugify_path

from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.

class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = ThumbnailerImageField(upload_to=slugify_path('imagenes/noticias'))
    publicada = models.DateTimeField(auto_now_add=True)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    votos = GenericRelation('votos.Voto')
    vistas = models.PositiveIntegerField(default=0)

    def institucion(self):
        if hasattr(self.creador, 'afiliacion'):
            return self.creador.afiliacion.institucion.nombre
        else:
            return 'Me Apunto'

    def as_dict(self, preview=False, viewer=None):
        res = {
            'id': self.id,
            'titulo': self.titulo,
            'imagen': image_to_dataURI(self.imagen['medium']),
            'publicada': self.publicada.isoformat(),
            'institucion': self.institucion(),
            'vistas': self.vistas
        }

        if not preview:
            res.update({
                'institucion': self.creador.afiliacion.institucion.as_dict(preview=True, viewer=viewer) if hasattr(self.creador, 'afiliacion') else 'Me Apunto',
                'descripcion': self.descripcion,
                'imagen': image_to_dataURI(self.imagen['large']),
                'votos': self.votos.count()
            })
            
        res['me_llega'] = self.votos.filter(usuario=viewer).exists()

        return res

    def save(self, *args, **kwargs):
        nuevo = self.id is None

        super(Noticia, self).save(*args, **kwargs)
        
        if nuevo:
            send_push_noticia(self, User.objects.filter(privacidad__recibir_notificaciones=True).all())

    def __unicode__(self):
        return u'%s' % self.titulo

    class Meta:
        ordering = ['-publicada']