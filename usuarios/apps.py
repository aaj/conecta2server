from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    name = 'usuarios'
    verbose_name = "Usuarios"

    def ready(self):
        import signals