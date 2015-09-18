from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Logro

@receiver(m2m_changed, sender=Logro.usuarios.through)
def logro_asignado(sender, instance, action, **kwargs):
    if action == 'post_add':
        print("LOGRO ASIGNADO, Enviando push...")
        print(action)
        print(instance)

        post_data = {
            "user_ids": [str(instance.id)],
            "notification": {"alert":"Hello World!"}
        }

        # app_id = YOUR_APP_ID
        # private_key = YOUR_PRIVATE_API_KEY
        # url = "https://push.ionic.io/api/v1/push"
        # req = urllib2.Request(url, data=post_data)
        # req.add_header("Content-Type", "application/json")
        # req.add_header("X-Ionic-Application-Id", app_id)
        # b64 = base64.encodestring('%s:' % private_key).replace('\n', '')
        # req.add_header("Authorization", "Basic %s" % b64)
        # resp = urllib2.urlopen(req)