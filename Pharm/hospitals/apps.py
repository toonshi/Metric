#apps.py
from django.apps import AppConfig


class HospitalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospitals'

    def ready(self):
        import hospitals.signals  # Import signals module
        from . import location
        location.run_script()