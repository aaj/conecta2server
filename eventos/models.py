import StringIO
import uuid
import qrcode
import qrcode.image.pil
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.fields import GenericRelation

from geoposition.fields import GeopositionField
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    lugar = GeopositionField()
    direccion = models.CharField(max_length=100)
    institucion = models.ForeignKey('instituciones.Institucion', related_name='eventos')
    imagen = ThumbnailerImageField(upload_to='imagenes/eventos')
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Participacion', related_name='participaciones')
    
    codigo_qr = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    imagen_qr = ThumbnailerImageField(upload_to='imagenes/eventos/qr', editable=False, blank=True)

    votos = GenericRelation('votos.Voto')
    vistas = models.PositiveIntegerField(default=0)

    def duracion(self):
        #float, en horas
        segundos = (self.fin - self.inicio).total_seconds()
        horas = segundos / 3600
        return horas

    def clean(self):
        if self.inicio and self.fin:
            if self.inicio == self.fin:
                raise ValidationError('El evento no puede comenzar y finalizar a la misma hora.')
            elif self.inicio > self.fin:
                raise ValidationError('El evento no puede comenzar despues de finalizar (Fecha de inicio esta DESPUES de Fecha de finalizacion).')

    def save(self, *args, **kwargs):
        if not self.codigo_qr:
            self.codigo_qr = uuid.uuid4()

        while Evento.objects.filter(codigo_qr=self.codigo_qr).exclude(id=self.id).exists():
            self.codigo_qr = uuid.uuid4()

        if not self.imagen_qr or self.codigo_qr not in self.imagen_qr.name:
            factory = qrcode.image.pil.PilImage
            img = qrcode.make(self.codigo_qr, image_factory=factory)
            
            djimg = StringIO.StringIO()
            img._img.save(djimg, format='PNG')

            self.imagen_qr = InMemoryUploadedFile(djimg, None, '%s.png' % self.codigo_qr, 'image/png', djimg.len, None)

            super(Evento, self).save(*args, **kwargs)


    def __unicode__(self):
        return '%s - %s' % (self.nombre, self.institucion.nombre)

    class Meta:
        ordering = ['-inicio']


class Logro(models.Model):
    nombre = models.CharField(max_length=50)
    evento = models.OneToOneField('Evento')
    imagen = ThumbnailerImageField(upload_to='imagenes/logros')
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='logros', blank=True)

    def descripcion(self):
        return 'Atendio al evento "%s".' % self.evento.nombre

    def save(self, *args, **kwargs):
        super(Logro, self).save(*args, **kwargs)

        # OJO: Esto no funciona en el admin de django. Por un problema raro.
        # Tuve que duplicar este codigo en el LogroAdmin en admin.py, para que
        # funcione aya.
        for usuario in self.evento.participantes.filter(participacion__verificada=True).all():
            if not usuario.logros.filter(id=self.id).exists():
                self.usuarios.add(usuario)

    def __unicode__(self):
        return '%s' % self.nombre


class Participacion(models.Model):
    evento = models.ForeignKey('Evento')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    verificada = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Participacion, self).save(*args, **kwargs)
        # Aqui se asignan logros a usuarios que participan a un evento, siemprey cuando
        # el evento tenga un logro asociado y la participacion haya sido verificada
        # (mediante el codigo qr).

        try:
            if self.verificada:
                self.evento.logro.usuarios.add(self.usuario)
            else:
                self.evento.logro.usuarios.remove(self.usuario)
        except Logro.DoesNotExist:
            pass #Este evento no tiene logro asignado

    def __unicode__(self):
        return '%s - %s' % (self.evento.nombre, self.usuario.get_full_name())


class Recuerdo(models.Model):
    evento = models.ForeignKey('Evento')
    imagen = ThumbnailerImageField(upload_to='imagenes/eventos/recuerdos')

    def __unicode__(self):
        return '%s (%s)' % (self.evento.nombre, self.imagen.name)