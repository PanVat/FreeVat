from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Naimportuje soubor 'signals.py'
    def ready(self):
        import users.signals
