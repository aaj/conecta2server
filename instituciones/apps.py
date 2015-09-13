from django.apps import AppConfig

class InstitucionesConfig(AppConfig):
    name = 'instituciones'
    verbose_name = "Instituciones"

    def ready(self):
        import signals