from django.apps import AppConfig


class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main_app'
    verbose_name = 'Main App'
    
    def ready(self):
        import main_app.signals
