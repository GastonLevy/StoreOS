from django.apps import AppConfig

class LogsConfig(AppConfig):
    """
    Configuration for the 'self_logs' app, which registers signals to log actions on models.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'self_logs'

    def ready(self):
        """
        Runs when Django starts. Imports the signals to ensure they are registered.
        """
        import self_logs.signals
