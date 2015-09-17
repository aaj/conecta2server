from django.apps import AppConfig

class EventosConfig(AppConfig):
    name = 'eventos'
    verbose_name = "Eventos"

    def ready(self):
        import signals