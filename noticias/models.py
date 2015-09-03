from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='imagenes/noticias')
    publicada = models.DateTimeField(auto_now_add=True)
    creador = models.OneToOneField(settings.AUTH_USER_MODEL)
    votos = GenericRelation('votos.Voto')
    vistas = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return '%s' % self.titulo

    class Meta:
        ordering = ['-publicada']