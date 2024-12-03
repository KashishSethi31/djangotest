# busdash/apps.py

from django.apps import AppConfig

class BusdashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'busdash'

    def ready(self):
        import busdash.dash_app  # Ensure this line imports the Dash app
