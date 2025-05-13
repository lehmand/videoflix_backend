from django.apps import AppConfig


class VideosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos'

    def ready(self):
        """
        This method is called when the Django application is fully loaded.
        It imports the signals module to ensure that all signal handlers are registered.
        
        The import is placed here instead of at the module level to avoid circular imports
        and to guarantee that the signal handlers are connected only when the app is ready.
        This is essential for Django's signal system to work properly with the Video model signals.
        """
        from . import signals
