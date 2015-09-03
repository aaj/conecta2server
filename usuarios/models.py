from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

class Perfil(models.Model):
    SEXO_CHOICES = (('f', 'Femenino'), ('m', 'Masculino'))
    
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    bio = models.CharField(max_length=1000, blank=True)

    correo_publico = models.BooleanField(default=True)
    telefono_publico = models.BooleanField(default=True)

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

    def __unicode__(self):
        return '%s (%d%% complete)' % (self.usuario.get_full_name() or self.usuario, self.porcentaje())


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