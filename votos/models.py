from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from easy_thumbnails.fields import ThumbnailerImageField
# Create your models here.

class Voto(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return '%s +1 %s' % (self.usuario, self.content_object)

    class Meta:
        unique_together = ('usuario', 'content_type', 'object_id')