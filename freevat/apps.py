from django.apps import AppConfig

class ModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'freevat'

    # Připojení 'signals.py' při startu (soubor, který obsahuje logiku pro 'models.py')
    def ready(self):
        import freevat.signals