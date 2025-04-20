from django.apps import AppConfig



class LandhubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'landhub'


    def ready(self):
        import landhub.signals
