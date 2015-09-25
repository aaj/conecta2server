import StringIO
import uuid
import qrcode
import qrcode.image.pil
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from conecta2.utils import image_to_dataURI, send_push_logro, send_push_evento

from geoposition.fields import GeopositionField
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    lugar = GeopositionField()
    direccion = models.CharField(max_length=100)
    institucion = models.ForeignKey('instituciones.Institucion', related_name='eventos')
    imagen = ThumbnailerImageField(upload_to='imagenes/eventos')
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Participacion', related_name='eventos')
    
    codigo_qr = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    imagen_qr = ThumbnailerImageField(upload_to='imagenes/eventos/qr', editable=False, blank=True)

    votos = GenericRelation('votos.Voto')
    vistas = models.PositiveIntegerField(default=0)

    def duracion(self):
        #float, en horas
        segundos = (self.fin - self.inicio).total_seconds()
        horas = segundos / float(3600)
        return horas

    def participacion(self, usuario=None):
        existe = False
        verificada = False

        if usuario:
            p = Participacion.objects.filter(evento=self, usuario=usuario).first()

            existe = p is not None
            verificada = p.verificada if p is not None else False
        
        return {'existe': existe, 'verificada': verificada}

    def participantes_count(self):
        return self.participantes.count()

    def participantes_verificados_count(self):
        return self.participantes.filter(participacion__verificada=True).count()
        
    def votos_count(self):
        return self.votos.count()

    def clean(self):
        if self.inicio and self.fin:
            if self.inicio == self.fin:
                raise ValidationError('El evento no puede comenzar y finalizar a la misma hora.')
            elif self.inicio > self.fin:
                raise ValidationError('El evento no puede comenzar despues de finalizar (Fecha de inicio esta DESPUES de Fecha de finalizacion).')

    def as_dict(self, preview=False, viewer=None):
        res = {
            'id': self.id,
            'nombre': self.nombre,
            'imagen': image_to_dataURI(self.imagen['large']),
            'lugar': {'lat': float(self.lugar.latitude), 'lng': float(self.lugar.longitude), 'description': self.direccion},
            'inicio': self.inicio.isoformat(),
            'fin': self.fin.isoformat(),
            'votos': self.votos_count(),
            'vistas': self.vistas,
            'institucion': self.institucion.as_dict(preview=preview)
        }

        if preview:
            res['participantes'] = self.participantes_count()
        else:
            res['participantes'] = list(self.participantes.all().values_list('id', flat=True))
            res['descripcion'] = self.descripcion

        res['me_llega'] = self.votos.filter(usuario=viewer).exists()
        res['participacion'] = self.participacion(usuario=viewer)

        return res

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

        nuevo = self.id is None:
        
        super(Evento, self).save(*args, **kwargs)

        if nuevo:
            send_push_evento(self, User.objects.all())

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

    def as_dict(self):
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion(),
            'imagen': image_to_dataURI(self.imagen['large']),
            'evento': {
                'id': self.evento.id,
                'nombre': self.evento.nombre,
                'imagen': image_to_dataURI(self.evento.imagen['medium']),
                'inicio': self.evento.inicio.isoformat(),
                'institucion': {
                    'id': self.evento.institucion.id,
                    'nombre': self.evento.institucion.nombre,
                    'logo': image_to_dataURI(self.evento.institucion.logo['medium'])
                }
            }
        }

    def save(self, *args, **kwargs):
        super(Logro, self).save(*args, **kwargs)

        # OJO: Esto no funciona en el admin de django. Por un problema raro.
        # Tuve que duplicar este codigo en el LogroInline en admin.py, para que
        # funcione aya.
        usuarios = list()

        for usuario in self.evento.participantes.filter(participacion__verificada=True).all():
            if not usuario.logros.filter(id=self.id).exists():
                usuario.logros.add(self)
                usuarios.append(usuario)

        if len(usuarios) > 0:
            send_push_logro(self, usuarios)

    def __unicode__(self):
        return '%s' % self.nombre


class Participacion(models.Model):
    evento = models.ForeignKey('Evento')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    verificada = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Participacion, self).save(*args, **kwargs)
        # Aqui se asignan logros a usuarios que participan a un evento, siempre y cuando
        # el evento tenga un logro asociado y la participacion haya sido verificada
        # (mediante el codigo qr).

        try:
            if self.verificada:
                if not self.usuario.logros.filter(id=self.evento.logro.id).exists():
                    self.usuario.logros.add(self.evento.logro)
                    send_push_logro(self.evento.logro, self.usuario)

            else: # ESTO NO VA! SOLO ES PARA DESARROLLO! LOS LOGROS NO SE LE QUITAN AL USUARIO, BAJO NINGUNA CIRCUNSTANCIA
                self.usuario.logros.remove(self.evento.logro)
        except Logro.DoesNotExist:
            pass #Este evento no tiene logro asignado. Ni modo.

    def __unicode__(self):
        return '%s - %s' % (self.evento.nombre, self.usuario.get_full_name())

    class Meta:
        verbose_name_plural = 'participaciones'
        unique_together = ('evento', 'usuario')


class Recuerdo(models.Model):
    evento = models.ForeignKey('Evento', related_name='recuerdos')
    imagen = ThumbnailerImageField(upload_to='imagenes/eventos/recuerdos')

    def as_dict(self, preview=False):
        if preview:
            return {'id': self.id, 'evento': self.evento.id, 'imagen': image_to_dataURI(self.imagen['medium'])}
        else:
            return {'id': self.id, 'evento': self.evento.id, 'imagen': image_to_dataURI(self.imagen)}

    def __unicode__(self):
        return '%s (%s)' % (self.evento.nombre, self.imagen.name)