from django.apps import AppConfig

class UsersConfig(AppConfig):
    """
    Configuration for the 'users' app. Loads signals on startup.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Import signals when the app starts to connect signal handlers
        import users.signals
